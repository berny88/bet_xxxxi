<template>
        <div class="container col-12">

            <h1><center>The ranking</center></h1>
            <div v-if="loading" class="loading">
            Loading...
            </div>

            <div v-if="error" class="error">
            {{ error }}
        </div>
        <div class="btn-group btn-group-block">
            <button class="btn" v-on:click="activePanel = 'global'">Global Ranking</button>
            <button class="btn" v-on:click="activePanel = 'byGame'">Ranking game by game</button>
            <button class="btn" v-on:click="activePanel = 'final'">Ranking Final phase</button>
            <button class="btn" v-on:click="activePanel = 'groupe'">Ranking Groupe</button>
        </div> 

        <div v-if="activePanel==='byGame'" class="error">
            <!--date, game_ta, result_ta, game_tb, result_tb,nickName , resultA, resultB, nbPoints-->
            <table class="table  table-striped table-hover">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Team A</th>
                        <th>Result A</th>
                        <th>Team B</th>
                        <th>Result B</th>
                        <th>Nickname</th>
                        <th>Bet A</th>
                        <th>Bet B</th>
                        <th>nbPoints</th>
                    </tr>
                </thead>
                <tbody id="v-for-object">
                    <tr v-for="p in rankings" :key="p.key">
                        <td > {{ p.date }}</td>
                        <td > {{ p.game_ta }}</td>
                        <td > {{ p.result_ta }}</td>
                        <td > {{ p.game_tb }}</td>
                        <td > {{ p.result_tb }}</td>
                        <td > {{ p.nickName }}</td>
                        <td > {{ p.resultA }}</td>
                        <td > {{ p.resultB }}</td>
                        <td > {{ p.nbPoints }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="activePanel==='global'" class="error">
            <!--date, game_ta, result_ta, game_tb, result_tb,nickName , resultA, resultB, nbPoints-->
            <table class="table  table-striped table-hover">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Avatar</th>
                        <th>Nickname</th>
                        <th>nbPoints</th>
                    </tr>
                </thead>
                <tbody id="v-for-object">
                    <tr v-for="p in globalRankings" :key="p.nickName">
                        <td > {{ p.rank }}</td>
                        <td>
                            <figure class="avatar avatar-xl" style="background-color: #5755d9;">
                        <!-- /apiv1.0/users/<user_id>/avatar-->
                            <img v-bind:src="p.imgurl" alt="">
                            </figure>
                        </td>
                        <td > {{ p.nickName }}</td>
                        <td > {{ p.cumul }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="activePanel==='final'" class="error">
                <!--date, game_ta, result_ta, game_tb, result_tb,nickName , resultA, resultB, nbPoints-->
                <table class="table  table-striped table-hover">
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Avatar</th>
                            <th>Nickname</th>
                            <th>nbPoints</th>
                        </tr>
                    </thead>
                    <tbody id="v-for-object">
                        <tr v-for="p in finalRankings" :key="p.nickName">
                            <td > {{ p.rank }}</td>
                            <td>
                                <figure class="avatar avatar-xl" style="background-color: #5755d9;">
                            <!-- /apiv1.0/users/<user_id>/avatar-->
                                <img v-bind:src="p.imgurl" alt="">
                                </figure>
                            </td>
                            <td > {{ p.nickName }}</td>
                            <td > {{ p.cumul }}</td>
                        </tr>
                    </tbody>
                </table>
        </div>
        <div v-if="activePanel==='groupe'" class="error">
            <!--date, game_ta, result_ta, game_tb, result_tb,nickName , resultA, resultB, nbPoints-->
            <table class="table  table-striped table-hover">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Avatar</th>
                        <th>Nickname</th>
                        <th>nbPoints</th>
                    </tr>
                </thead>
                <tbody id="v-for-object">
                    <tr v-for="p in groupeRankings" :key="p.nickName">
                        <td > {{ p.rank }}</td>
                        <td>
                            <figure class="avatar avatar-xl" style="background-color: #5755d9;">
                        <!-- /apiv1.0/users/<user_id>/avatar-->
                            <img v-bind:src="p.imgurl" alt="">
                            </figure>
                        </td>
                        <td > {{ p.nickName }}</td>
                        <td > {{ p.cumul }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
</template>
<script>
    import axios from "axios";

export default {
    data () {
        return {
        loading: false,
        rankings: [{ title: 'Foo' }, { title: 'Bar' }],
        globalRankings: [{ title: 'Foo' }, { title: 'Bar' }],
        error: null,
        activePanel:"global"
        }
    },
    created () {
        // fetch the data when the view is created and the data is
        // already being observed
        this.fetchData()
    },
    watch: {
        // call again the method if the route changes
        '$route': 'fetchData'
    },
    methods: {
        switchPanel (name) {
            this.activePanel=name;
        },
        fetchData () {
            this.error = this.post = null;
            this.loading = true;
            var connect_attr={};
            axios({ method: "GET", "url": "back/matchs/apiv1.0/matchs/ranking", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                        //date, game_ta, result_ta, 
                        //game_tb, result_tb, 
                        //nickName , resultA, resultB, nbPoints
                            this.rankings = result.data.rankings;
                            this.loading = false;
                            console.info("rankings", this.rankings)
                               

                            }, error => {
                                console.error(error);
                                this.errormsg=error;
                                this.error = error.toString();
                            }
            );
            axios({ method: "GET", "url": "back/matchs/apiv1.0/matchs/global_rankings", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                        //date, game_ta, result_ta, 
                        //game_tb, result_tb, 
                        //nickName , resultA, resultB, nbPoints
                            this.globalRankings = result.data.globalRankings;
                            this.loading = false;
                            console.info("globalRankings", this.globalRankings)
                            for (let i = 0; i < this.globalRankings.length; i++) {
                                this.globalRankings[i].imgurl = "/back/users/apiv1.0/users/" + this.globalRankings[i].uuid+"/avatar";
                            }        
                            }, error => {
                                console.error(error);
                                this.errormsg=error;
                                this.error = error.toString();
                            }
            );
            axios({ method: "GET", "url": "back/matchs/apiv1.0/matchs/final_rankings", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                        //date, game_ta, result_ta, 
                        //game_tb, result_tb, 
                        //nickName , resultA, resultB, nbPoints
                            this.finalRankings = result.data.finalRankings;
                            this.loading = false;
                            console.info("finalRankings", this.finalRankings)
                            for (let i = 0; i < this.finalRankings.length; i++) {
                                this.finalRankings[i].imgurl = "/back/users/apiv1.0/users/" + this.finalRankings[i].uuid+"/avatar";
                            }        
                            }, error => {
                                console.error(error);
                                this.errormsg=error;
                                this.error = error.toString();
                            }
            );
            axios({ method: "GET", "url": "back/matchs/apiv1.0/matchs/groupe_rankings", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                        //date, game_ta, result_ta, 
                        //game_tb, result_tb, 
                        //nickName , resultA, resultB, nbPoints
                            this.groupeRankings = result.data.groupeRankings;
                            this.loading = false;
                            console.info("groupeRankings", this.groupeRankings)
                            for (let i = 0; i < this.groupeRankings.length; i++) {
                                this.groupeRankings[i].imgurl = "/back/users/apiv1.0/users/" + this.groupeRankings[i].uuid+"/avatar";
                            }        
                            }, error => {
                                console.error(error);
                                this.errormsg=error;
                                this.error = error.toString();
                            }
            );
            
        }
    }
}
</script>