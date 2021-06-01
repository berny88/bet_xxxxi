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
                                Team B
                            </th>
                        </tr>
                    </thead>
                    <tbody id="v-for-object">
                        <tr v-for="p in posts" :key="p.title">
                            <td > {{ p.title }}</td>
                            <td > {{ p.body }}</td>
                            <td ><span class="newflags FRA"></span> ta</td>
                            <td ><input style="width:50px;text-align:center;" value="FRA" disabled></td>
                            <td ><input style="width:50px;text-align:center;" value="GER" disabled></td>
                            <td ><span class="newflags GER"></span> GER</td>
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
        posts: [{ title: 'Foo' }, { title: 'Bar' }],
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
                            this.errormsg = result.data;
                            this.loading = false;
                            this.posts = [{title:"ponpon", body:"thebodyponpon"},
                            {title:"podddddnpon", body:"thebodyponpondddddd"},
                            {title:"pdddddodddddnpon", body:"333333thebodyponpondddddd"},
                            ];
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