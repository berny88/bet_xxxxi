
<template>
  <div id="app">
    <div class="container grid-960">
      <div class="columns">
          <div class="column">

            <header class="navbar">
            <section class="navbar-section">
              <ul>
                <li><router-link to="/" class="btn btn-link">Home</router-link> </li>
                <li><router-link to="/bets" class="btn btn-link">Bets</router-link> </li>
                <li><router-link to="/games" class="btn btn-link">Games</router-link> </li>
                <li><router-link to="/users" class="btn btn-link">Betors</router-link> </li>
                <li><router-link to="/ranking" class="btn btn-link">Ranking</router-link> </li>
                <li><router-link to="/about" class="btn btn-link">About</router-link></li>
              </ul>
            </section>
          </header>
          <router-view/>
          </div>
        </div>
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
#nav {
  padding: 30px;
}
#nav a {
  font-weight: bold;
  color: #2c3e50;
}
#nav a.router-link-exact-active {
  color: #42b983;
}

.nav-default {
  background-color: #efefef;
  padding: 1rem;
  border-radius: .3rem;
}

.navbar {
  flex-flow: row wrap;
}

.navbar-section,
.navbar-section ul {
  display: flex;
}

.navbar-section ul {
  margin: 0 0 0 2rem;
}

.navbar-section li {
  list-style: none;
  margin: 0;
  padding: 0 5px;
}

.btn.btn-link:hover {
  background: #5764c6 none repeat scroll 0 0;
  border-color: #4452c0;
  color: #ffffff;
}

@media screen and (min-width:10em) and (max-width:46em) {
  .navbar {
    flex-flow: column wrap;
    align-items: stretch;
  }
  .navbar-header {
    display: flex;
    justify-content: space-between;
    flex-direction: row;
  }
  .navbar-section {
    display: flex;
    flex-flow: row wrap;
    margin-top: 15px;
  }
  .navbar-section ul {
    flex-flow: row wrap;
    margin: 2rem 0 0;
  }
  .navbar-section ul li {
    padding: 5px;
  }
}

@media screen and (max-width:25em) {
  .navbar-section ul {
    flex-flow: column wrap;
    width: 100%;
  }
  .navbar-section ul a {
    width: 100%;
  }
}

</style>