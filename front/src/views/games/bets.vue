<template>
        <div class="container grid-xs">

            <h1><center>Your bets</center></h1>
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>
    <div v-if="msg" class="toast toast-success">
      {{ msg }} <br/>
    </div>

    <div class="col-xs-12">

                <table class="table  table-striped table-hover">
                    <thead>
                        <tr>
                            <th >
                                Date                                
                            </th>
                            <th>
                                Group                                
                            </th>
                            <th>
                               Team A
                               </th>
                            <th>
                            </th>
                            <th>
                            </th>
                            <th>
                            </th>
                            <th>
                            </th>
                            <th>
                                Team B
                            </th>
                        </tr>
                    </thead>
                    <tbody id="v-for-object">
                        <tr v-for="p in games" :key="p.key">
                            <td > {{ p.dateMatch }}</td>
                            <td > {{ p.category }}</td>
                            <td > {{ p.libteamA }}</td>
                            <td ><span class="newflags FRA"></span> </td>
                            <td ><input style="width:50px;text-align:center;" 
                                    :name="resultA" :id="resultA" v-model="p.resultA"></td>
                            <td ><input style="width:50px;text-align:center;" 
                                    :name="resultB" :id="resultB" v-model="p.resultB"></td>
                            <td ><span class="newflags GER"></span> </td>
                            <td > {{ p.libteamB }}</td>
                        </tr>
                    </tbody>
                </table>
                    <div v-if="loading" class="loading">
                    Loading...
                    </div>

                    <div v-if="error" class="error">
                    {{ error }}
                    </div>
                    <div v-if="msg" class="toast toast-success">
                    {{ msg }} <br/>
                    </div>
                <button id="submit"  v-on:click="save()" class="btn btn-success">
                    Never forget to save !</button>

            </div>
        </div>
</template>
<script>
    import axios from "axios";

export default {
    data () {
        return {
        loading: false,
        games: [],
        error: null
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
        fetchData () {
            if (this.$store.state.uid != "") {
                this.error = this.post = null;
                this.loading = true;            
                var connect_attr={};
                console.info("load bets for ", this.$store.state.uid);
                axios({ method: "GET", "url": "back/matchs/apiv1.0/matchs/"+ this.$store.state.uid +"/bets", 
                        "data": {connect: connect_attr}, 
                        "headers": { "content-type": "application/json" } }).then(result => {
                                //{"category":"GRPA","date":"2021/06/11 21:00:00","key":"GRPA-TURITA","libteamA":"Turkey","libteamB":"Italia","resultA":null,"resultB":null,"teamA":"TUR","teamB":"ITA"}
                                this.games = result.data.bets;
                                this.loading = false;
                                
                                }, error => {
                                    console.error(error);
                                    this.errormsg=error;
                                    this.error = error.toString();
                                }
                );
            }else{
               this.error="please connect you before"; 
            }
            
        },
        save () {
            this.error = this.post = null;
            this.loading = true;
            var connect_attr={"bets":this.games};
            console.info("save bets for ", this.$store.state.uid);
            console.info("save bets for ", this.games);
            axios({ method: "POST", "url": "back/matchs/apiv1.0/matchs/"+ this.$store.state.uid +"/bets", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                            //{"category":"GRPA","date":"2021/06/11 21:00:00","key":"GRPA-TURITA","libteamA":"Turkey","libteamB":"Italia","resultA":null,"resultB":null,"teamA":"TUR","teamB":"ITA"}
                            console.info("result save ", result.data);
                            this.msg = result.data.data;
                            this.loading = false;
                            
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