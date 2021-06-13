 
<template>
  <div id="app">
      <header class="navbar">
        <section class="navbar-section">
          <router-link to="/" class="a btn btn-link">Home</router-link>
          <router-link to="/bets" class="a btn btn-link">Bets</router-link>
          <router-link to="/games" class="a btn btn-link">Games</router-link>
          <router-link to="/users" class="a btn btn-link">Bettors</router-link>
          <router-link to="/ranking" class="a btn btn-link">Ranking</router-link>
          <router-link to="/about" class="a btn btn-link">About</router-link>
        </section>
      </header> 
      <router-view/>
  </div>
</template>

<script>
    export default {
        name: 'App',
        data() {
            return {
                mockAccount: {
                    email: "nraboy",
                    thepwd: "password"
                }
            }
        },
        mounted() {
            if(!this.$store.state.isConnected) {
                this.$router.replace({ name: "Signin" });
            }
        },
        methods: {
            logout() {
                this.$store.state.isConnected = false;
            }
        }
    }
</script>

<style>
  @import 'https://unpkg.com/spectre.css/dist/spectre.min.css';
  @import 'https://unpkg.com/spectre.css/dist/spectre-exp.min.css';
  @import 'https://unpkg.com/spectre.css/dist/spectre-icons.min.css';

  #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  }



</style>