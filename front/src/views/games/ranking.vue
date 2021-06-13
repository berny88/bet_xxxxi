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
        </div> 

            <div v-if="activePanel==='byGame'" class="error">
                <!--date, game_ta, result_ta, game_tb, result_tb,nickName , resultA, resultB, nbPoints-->
                <table class="table  table-striped table-hover">
                    <thead>
                        <tr>
                            <th >Date</th>
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
                            <th>Nickname</th>
                            <th>nbPoints</th>
                        </tr>
                    </thead>
                    <tbody id="v-for-object">
                        <tr v-for="p in globalRankings" :key="p.nickName">
                            <td > {{ p.rank }}</td>
                            <td > {{ p.nickName }}</td>
                            <td > {{ p.cumul }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
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