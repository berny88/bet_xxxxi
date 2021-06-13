<template>
        <div class="container grid-xs">

            <h1><center>The games</center></h1>
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div class="col-xs-12">

                <table class="table  table-striped table-hover">
                    <thead>
                        <tr>
                            <th >Date</th>
                            <th>Team A</th>
                            <th></th>
                            <th></th>
                            <th></th>
                            <th></th>
                            <th>Team B</th>
                        </tr>
                    </thead>
                    <tbody id="v-for-object">
                        <tr v-for="p in games" :key="p.key">
                            <td > {{ p.date }}</td>
                            <td > {{ p.libteamA }}</td>
                            <td ><span class="newflags FRA"></span> </td>
                            <td ><input style="width:50px;text-align:center;" v-model="p.resultA" disabled></td>
                            <td ><input style="width:50px;text-align:center;" v-model="p.resultB" disabled></td>
                            <td ><span class="newflags GER"></span> </td>
                            <td > {{ p.libteamB }}</td>
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
        games: [{ title: 'Foo' }, { title: 'Bar' }],
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
            this.error = this.post = null;
            this.loading = true;
            var connect_attr={};
            axios({ method: "GET", "url": "back/matchs/apiv1.0/matchs", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                            //{"category":"GRPA","date":"2021/06/11 21:00:00","key":"GRPA-TURITA","libteamA":"Turkey","libteamB":"Italia","resultA":null,"resultB":null,"teamA":"TUR","teamB":"ITA"}
                            this.games = result.data.matchs;
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