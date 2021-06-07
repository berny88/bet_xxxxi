<template>
    <div class="container grid-xs form-group" >
        <div class="form-group required">
            <h1><span class="hero bg-gray"></span> You made the right choice !</h1>

            <label for="email" class="form-label">Enter your email address to register </label>
          <input type="email" class="form-input" id="email" v-model="email"
              placeholder="Votre email" value="" required="required">
          <script>
            $(function () {
              $('#email').focus();
            });
          </script>
        </div>
        <button type="submit"  v-on:click="save()" id="submit" name="submit" value="Sign in"
          class="btn btn-primary">Sign up now !</button>&nbsp;
          <a class="btn btn-error" href="/">Back</a><br/>
      <span>This email will be your user account. We will just use it to notify the daily ranking.<br/>
      We don't sell your personnal data because the GAFAM already have this informations.
      </span>
    </div>
</template>


<script>
    import axios from "axios";

   export default {
        data() {
            return {
                error:""
            }
        },
        watch: {
            // call again the method if the route changes
            '$route': ''
        },
        methods: {
            save() {
                var connect_attr={"email":this.email};
                console.info("connect_attrb", connect_attr)
                axios({ method: "POST", "url": "back/users/subscription", 
                    "data": {connect: connect_attr}, 
                    "headers": { "content-type": "application/json" } }).then(result => {
                                    this.uuid = result.data.uuid;                                    
                                    console.info("result",result.data);
                                    console.info("uid",this.uuid);
                                    // named route
                                    this.$router.push({ name: 'User', params: { uid: this.uuid } })
                                    }, error => {
                                        console.error(error);
                                        this.error=error;
                                    }
                                    );
            }
        }
    }
</script>

