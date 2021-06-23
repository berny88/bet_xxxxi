<template>
    <div class="container grid-xs">
        <div class="row-fluid" >
            <h1><center>Bettors</center></h1>
        </div>
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
                        <th>Avatar</th>
                        <th>Nickname</th>
                        <th>Description</th>
                        <th></th>
                    </tr>
                </thead>
                <tbody >
                    <tr v-for="b in betors" :key="b.uuid">
                        <td>
                            <figure class="avatar avatar-xl" style="background-color: #5755d9;">
                           <!-- /apiv1.0/users/<user_id>/avatar-->
                               <img v-bind:src="b.imgurl" alt="{{ b.nickName }}">
                            </figure>
                        </td>
                        <td>{{ b.nickName }} </td>
                        <td>{{ b.description }}</td>
                        <td></td>                            
                    </tr>
                </tbody>
            </table>

        </div>
    </div>
</template>
<script>
    import axios from "axios";

   
   export default {
        data() {
            return {
                betors: [],
                errormsg:""
            }
        },
        created () {
            // fetch the data when the view is created and the data is
            // already being observed
            this.getUsers()
        },
        watch: {
                // call again the method if the route changes
                '$route': 'getUsers'
        },
        methods: {
            getUsers() {
                var connect_attr={};
                axios({ method: "GET", "url": "back/users/apiv1.0/users", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                                    this.betors = result.data.users;
                                    for (let i = 0; i < this.betors.length; i++) {
                                        this.betors[i].imgurl = "/back/users/apiv1.0/users/" + this.betors[i].uuid+"/avatar";
                                    }
                                    console.info(this.betors);
                                    }, error => {
                                        console.error(error);
                                        this.errormsg=error;
                                    }
                                    );
            }
        }
    }
</script>