# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request, session
import logging
import math
import sqlite3

from back.tools.Tools import ToolManager
from back.tools.Tools import DbManager
from back.users.UserServices import UserManager
from back.bets.BetsServices import BetsManager

logger = logging.getLogger(__name__)

matchs_page = Blueprint('matchs_page', __name__,
                       template_folder='templates', static_folder='static')



@matchs_page.route('/matchslist', methods=['GET'])
def matchslist():
    return matchs_page.send_static_file('matchs.html')


@matchs_page.route('/apiv1.0/matchs', methods=['GET'])
def getMatchs():
    mgr = MatchsManager()
    matchs=mgr.getAllMatchs()
    logger.info(">>{}".format(jsonify({'matchs': matchs}).data))

    return jsonify({'matchs': matchs})

@matchs_page.route('/apiv1.0/matchs/ranking', methods=['GET'])
def getRankings():
    mgr = MatchsManager()
    rankings=mgr.getAllRanking()
    logger.info(">>{}".format(jsonify({'rankings': rankings}).data))

    return jsonify({'rankings': rankings})

@matchs_page.route('/apiv1.0/matchs/global_rankings', methods=['GET'])
def getGlobalRankings():
    mgr = MatchsManager()
    rankings=mgr.getRankings("")
    logger.info(">>{}".format(jsonify({'globalRankings': rankings}).data))

    return jsonify({'globalRankings': rankings})

@matchs_page.route('/apiv1.0/matchs/final_rankings', methods=['GET'])
def getFinalRankings():
    mgr = MatchsManager()
    rankings=mgr.getRankings("FIN")
    logger.info(">>{}".format(jsonify({'finalRankings': rankings}).data))

    return jsonify({'finalRankings': rankings})

@matchs_page.route('/apiv1.0/matchs/groupe_rankings', methods=['GET'])
def getGroupeRankings():
    mgr = MatchsManager()
    rankings=mgr.getRankings("GRP")
    logger.info(">>{}".format(jsonify({'groupeRankings': rankings}).data))

    return jsonify({'groupeRankings': rankings})


@matchs_page.route('/apiv1.0/matchs', methods=['PUT'])
def updateMatchsResults():
    u"""
    save the result of matchs.
    only allowed to admin
    :return the numbers of matchs updated
    """
    logger.info("updateMatchsResults::{}".format(request.json["connect"]))
    if "no_save" in request.json:
        no_save=request.json["no_save"]
    else:
        no_save=False
    logger.info("updateMatchsResults::no_save={}".format(no_save))
    if "cookieUserKey" in session:
        mgr = MatchsManager()
        matchsjson = request.json["connect"]
        cookieUserKey = session['cookieUserKey']
        user_mgr = UserManager()
        user = user_mgr.getUserByUserId(cookieUserKey)
        logger.info(u"updateMatchsResults::cookieUserKey by ={}".format(cookieUserKey))
        logger.info(u"updateMatchsResults::update by ={}".format(user.email))
        nbHit=0
        if user.isAdmin:
            listGame=matchsjson['bets']
            nbHit = mgr.update_all_matchs(listGame, no_save)
        else:
            logger.info(u"updateMatchsResults::No Admin = 403")
            return "Ha ha ha ! Mais t'es pas la bonne personne pour faire ça, mon loulou", 403
        return jsonify({'nbHit': nbHit})
    else:
        return "Ha ha ha ! Mais t'es qui pour faire ça, mon loulou ?", 403

@matchs_page.route('/apiv1.0/matchs/<user_id>/bets', methods=['GET'])
def getBets(user_id):
    u"""
    return the list of all bets of a user in a community.
    If user has never bet, we return the list of Matchs.
    :param com_id: id of community (uuid)
    :param user_id: id of user (uuid)
    :return:  a json form for the list of bet
    """
    mgr = MatchsManager()
    game_list = mgr.getAllMatchs()
            
    betsMgr = BetsManager()
    bets = betsMgr.getBetsOfUser(user_id, game_list)

    logger.debug(u" ------------ ")
    logger.debug(u"getBets::bets={}".format(bets))
    return jsonify({'bets': bets})

@matchs_page.route('/apiv1.0/matchs/<user_id>/bets', methods=['POST'])
def saveBets(user_id):
    u"""
    Save bets
    :param user_id: id of user (uuid)
    :return:  a json form for the list of bet
    """
    betslist = request.json["connect"]
    logger.info(u"saveBets::bets={} ".format(betslist))
    logger.info(u"saveBets::bets={} ".format(betslist["bets"]))

    cookieUserKey = session['cookieUserKey']
    logger.info(u"saveBets::cookieUserKey={} ".format(cookieUserKey))
    if (cookieUserKey == user_id):
        betsMgr = BetsManager()
        bets = betsMgr.createOrUpdateBets(user_id, betslist["bets"])
    #this.games
    logger.debug(u" ------------ ")
    logger.debug(u"getBets::bets={}".format(bets))
    return jsonify({'data': "great, U R the best !"})

u"""
**************************************************
Service layer
"""


class Match:
    u""""
     "key": "GROUPEE_SWE_BEL",
       "teamA": "SWE",
       "teamB": "BEL",
       "libteamA": "SUEDE",
       "libteamB": "BELGIQUE",
       "dateMatch": "22/06/2016 21:00:00",
       "dateDeadLineBet": "",
       "resultA": "",
       "resultB": "",
       "category": "GROUPE",
       "categoryName": "GROUPEE"
    """""
    def __init__(self):
        self.key = u""
        self.teamA = u""
        self.teamB = u""
        self.libteamA = u""
        self.libteamB = u""
        self.resultA=-1
        self.resultB=-1
        self.category = u""
        self.categoryName = u""


    def convertFromDict(self, elt):
        u"""
        convert a community object from mongo
        :param elt: bson data from mongodb
        :return: nothing
        """
        for k in elt.keys():
            if k == "_id":
                self._id = str(elt[k])
            else:
                self.__dict__[k] = elt[k]


    def convertIntoBson(self):
        u"""
        convert a community object into mongo Bson format
        :return: a dict to store in mongo as json
        """
        elt = dict()
        for k in self.__dict__:
            if k == "_id" and self._id is not None:
                elt[k] = ObjectId(self._id)
            else:
                elt[k] = self.__dict__[k]
        return elt


    def computeResult(self, bet):
        u"""
            Si le parieur a trouvé le vainqueur (ou deviné un match nul) : 5 points
            3 points si le parieur a deviné le nombre de point d'une équipe
            2 points si le parieur a deviné la bonne différence de points entre les 2 équipes (peu importe le vainqueur)
            Donc, pour chaque match, un parieur peut récolter 5 + 6 + 2 points = 13 points s'il devine le résultat exact du match
        """
        nb_point=0

        #tool = ToolManager()
        #str_nb=tool.getProperty(key="NB_POINT_TEAM")["value"]
        #if str_nb=="":
        NB_POINT_TEAM=3
        #else:
    #    NB_POINT_TEAM=int(str_nb)

    #str_nb=tool.getProperty(key="NB_POINT_WINNER")["value"]
        #    if str_nb=="":
        NB_POINT_WINNER=5
        #else:
    #    NB_POINT_WINNER=int(str_nb)

    #str_nb=tool.getProperty(key="NB_POINT_DIFF")["value"]
        #   if str_nb=="":
        NB_POINT_DIFF=2
        #else:
    #    NB_POINT_DIFF=int(str_nb)

        #change nbpoints only if rightmatch
        logger.info(u'\tMatchs::computeResult=bet={}'.format(bet))
        logger.info(u'\tMatchs::computeResult=game.key{}-bet.key{}'.format(self.key, bet.game_id))
        if (self.key==bet.game_id):
            if (self.resultA is not None) and (self.resultB is not None):            
                logger.info(u'\t\tMatchs::computeResult=bet.resA={} - self.resA={}'.format(bet.resultA,self.resultA))
                logger.info(u'\t\tMatchs::computeResult=bet.resB={} - self.resB={}'.format(bet.resultB,self.resultB))
                #3 points si le parieur a deviné le nombre de point d'une équipe
                if bet.resultA==self.resultA:
                    nb_point=nb_point+NB_POINT_TEAM
                if bet.resultB == self.resultB:
                    nb_point = nb_point + NB_POINT_TEAM
                # 2 points si le parieur a deviné la bonne différence de points entre les 2 équipes (peu importe le vainqueur)
                if math.fabs(self.resultA-self.resultB) == math.fabs(bet.resultA-bet.resultB):
                    nb_point = nb_point + NB_POINT_DIFF
                #5 pts if 1N2
                if  (((self.resultA-self.resultB) >0 and (bet.resultA-bet.resultB)>0) or
                    ((self.resultA - self.resultB) < 0 and (bet.resultA - bet.resultB) < 0) or
                    ((self.resultA - self.resultB) == 0 and (bet.resultA - bet.resultB) == 0)):
                    nb_point = nb_point+NB_POINT_WINNER
                logger.info(u'\t\tMatchs::computeResult=nb_point={}'.format(nb_point))
        #finally we update nb of points
        bet.nbPoints = nb_point

class MatchsManager(DbManager):

    def getAllMatchs(self):
        """
        get the complete list of matchs
        """
        localdb = self.getDb()

        """uuid, nickName, desc, avatar, email, isAdmin"""

        sql_all_games="""SELECT category, key, date, libteamA, teamA, libteamB, teamB,
            resultA, resultB
                        FROM GAME order by date, key;"""
        cur = localdb.cursor()
        cur.execute(sql_all_games)

        rows = cur.fetchall()
        result = list()
        for row in rows:
            result.append(row)                    
            logger.info("game={}".format(row))
        return result


    def update_all_matchs(self, matchs_to_update, no_save):
        #load all match from db (because we just want to update result
        logger.info(u"update_all_matchs::start-games to update {}".format(matchs_to_update))
        nb_hits=0
        bet_mgr = BetsManager()
        for m in matchs_to_update:
            match = Match()
            match.convertFromDict(m)
            match_key=match.key
            betList = bet_mgr.getBetsOfGame(match_key)
            if not no_save:
                # mettre à jour juste les resultats
                logger.info(u'\tupdate_all_matchs::try update game :{}'.format(m))
                try:
                    localdb = self.getDb()
                    c = localdb.cursor()
                    c.execute("""update GAME 
                                set resultA=?, resultB=?
                                where
                                key=?""", (match.resultA, match.resultB, match.key))  
                    localdb.commit()
                            
                except sqlite3.Error as e:
                    logger.error(e)
                    logger.info(u'\tid : {}'.format(bet))
                    localdb.rollback()
                    logger.info(u'update_all_matchs::rollback')
                nb_hits = nb_hits + 1
            else:
                logger.info("no match updated")
            
            # pour chaque match demander à betmanager de calculer le nb de points de chq bet
            # le principe sera de calculer le nbde pts d'un user = somme de ses paris
            for bet in betList:
                match.computeResult(bet)
                logger.info(
                    u'\t\tupdate_all_matchs::bet={}/{} - nbpts={}'.format(bet.game_id, bet.user_id, bet.nbPoints))
                bet_mgr.saveScore(bet)


        return None

    def getAllRanking(self):
        """
        get the complete list of matchs
        """
        localdb = self.getDb()

        """uuid, nickName, desc, avatar, email, isAdmin"""

        sql_all_ranking="""select g.date, g.libteamA as game_ta, g.resultA  as result_ta, 
                         g.libteamB as game_tb, g.resultB as result_tb, 
                         u.nickName , b.resultA, b.resultB, nbPoints
                        from BETUSER u, game g, BET b
                        where u.uuid=b.FK_USER
                        and b.FK_GAME=g.key
                        and g.resultA is not null
                        and g.resultB is not NULL
                        order by g.date desc, g.libteamA asc, nbPoints DESC, u.nickName COLLATE NOCASE ASC;"""
        cur = localdb.cursor()
        cur.execute(sql_all_ranking)

        rows = cur.fetchall()
        result = list()
        for row in rows:
            result.append(row)                    
            logger.info("getAllRanking::bet_result={}".format(row))
        return result
    

    def getRankings(self, phase):
        """
        @phase : if empty = global
        GRP = Groupe phase
        FIN = Final phase
        """
        localdb = self.getDb()

        """uuid, nickName, desc, avatar, email, isAdmin"""

        sql_global_ranking="""select u.uuid, u.nickName , sum(nbPoints) as cumul
                            from BETUSER u, BET b
                            where u.uuid=b.FK_USER
                            and b.FK_GAME like '{}%'
                            group by nickName
                            order by 3 desc;"""
        cur = localdb.cursor()
        cur.execute(sql_global_ranking.format(phase))

        rows = cur.fetchall()
        result = list()
        i=1
        for row in rows:
            row["rank"]=i
            result.append(row)                    
            logger.info("MatchServices::getRankings={}".format(row))
            i=i+1
        return result




