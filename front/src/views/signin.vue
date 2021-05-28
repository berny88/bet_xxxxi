<template>
    <div class="container grid-xs">
        <h1><center>Connection</center></h1>
        <!--p v-if="errors.length">
          <b>Please correct the following error(s):</b>
          <ul>
            <li v-for="err in errors" :key="err.message">{{ err.message }}</li>
          </ul>
        </p-->
        <div class="form-group">
          <form name="thelogin" ng-submit="login()" required>
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <input type="email" class="form-input" id="email" name="nom" v-model="email"
                placeholder="Your email" value="" required="required">
            </div>
            <div class="form-group">
              <label for="thepwd" class="form-label">Password</label>
              <input type="password" class="form-input" id="thepwd" name="thepwd" v-model="thepwd"
                    placeholder="Your password" value="" required="required">
            </div>
            <button type="submit" id="submit" name="submit" value="Sign in"
              class="btn btn-success">Login to your account !</button>
            <router-link to="/" class="btn btn-error" >Back</router-link>
          </form>
          <br/>
          <br/>
          <!--<a class="btn btn-default disabled" href="#signon">No account yet ?</a> Inscriptions closed for this event !-->
          <a class="btn btn-primary" href="#signon">No account yet ?</a>
        </div>
    </div>
</template>
