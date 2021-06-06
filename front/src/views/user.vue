<template>
    <div class="container grid-xs" id="signin">
        <h1><center>Connection</center></h1>
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

       <div class="form-group">
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input type="email" class="form-input" id="email" v-model="user.email"
                placeholder="Your email" value="" readonly="readonly">
            </div>
            <div class="form-group">
              <label for="thepwd" class="form-label">Password</label>
              <input type="password" class="form-input" id="thepwd"  v-model="user.thepwd"
                    placeholder="Your password" value="" required="required">
            </div>
            <div class="form-group">
                <label for="description" class="form-label">Description</label>
                <input type="description" class="form-input" id="description"  v-model="user.description"
                    placeholder="Description" value="" required="required">
            </div>
            <button id="submit"  v-on:click="save()" class="btn btn-success">
              Save</button>
            &nbsp;
            <router-link to="/" class="btn btn-error" >Back</router-link>
          <br/>
        </div>
    </div>

</template>

<script>
    import axios from "axios";

   export default {
        data() {
            return {
                user: {'email':'', 'thepwd':'', 'description':''},
                error:""
            }
        },
        created () {
            // fetch the data when the view is created and the data is
            // already being observed
            this.getUser()
        },
        watch: {
            // call again the method if the route changes
            '$route': 'getUser'
        },
        methods: {
            getUser() {
                let params = this.$route.query
                console.log(params)

                let uid = this.$route.query.uid
                console.log(uid)
                var connect_attr={};
                axios({ method: "GET", "url": "back/users/apiv1.0/users/"+uid, 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                                    this.user = result.data.user;                                    
                                    console.info(this.user);
                                    }, error => {
                                        console.error(error);
                                        this.error=error;
                                    }
                                    );
            }
        }
    }
</script>