<template>
        <div class="container grid-xs">

            <h1><center>To bets</center></h1>

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
                    <tbody >
                        <tr >
                            <td >date</td>
                            <td >categ</td>
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
        name: 'bets',
        data() {
            return {
                input: {
                    email: "",
                    thepwd: ""
                },
                errormsg:""
            }
        },
        methods: {
            bets_list() {
                if(this.input.email != "" && this.input.thepwd != "") {
                    this.$emit("authenticated", true);
                    var connect_attr={email:this.input.email, thepwd:this.input.thepwd};
                        axios({ method: "POST", "url": "back/users/apiv1.0/login", 
                        "data": {connect: connect_attr}, 
                        "headers": { "content-type": "application/json" } }).then(result => {
                    this.errormsg = result.data;
                    this.$router.replace({ name: "Bets" });
                    }, error => {
                        console.error(error);
                        this.errormsg=error;
                    });
                } else {
                    console.log("A email and password must be present");
                }
            }
        }
    }
</script>