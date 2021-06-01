<template>
    <div class="container grid-xs" id="signin">
        <h1><center>Connection</center></h1>
    
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
            <div class="form-group">
                <label for="description" class="form-label">Description</label>
                <input type="description" class="form-input" id="description"  v-model="input.description"
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