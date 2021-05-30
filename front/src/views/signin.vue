<template>
    <div class="container grid-xs" id="signin">
        <h1><center>Connection</center></h1>
        <p v-if="errormsg!=''">
          <b>{{ errormsg }}</b>
        </p>
        
        <div class="form-group">
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input type="email" class="form-input" id="email" v-model="input.email"
                placeholder="Your email" value="" required="required">
            </div>
            <div class="form-group">
              <label for="thepwd" class="form-label">Password</label>
              <input type="password" class="form-input" id="thepwd"  v-model="input.thepwd"
                    placeholder="Your password" value="" required="required">
            </div>
            <button id="submit"  v-on:click="login()" class="btn btn-success">
              Login to your account !</button>
            &nbsp;
            <router-link to="/" class="btn btn-error" >Back</router-link>
          <br/>
          <!--<a class="btn btn-default disabled" href="#signon">No account yet ?</a> Inscriptions closed for this event !-->
          <a class="btn btn-primary" href="#signon">No account yet ?</a>
        </div>
    </div>
</template>

<script>
    import axios from "axios";

   export default {
        name: 'Login',
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
            login() {
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