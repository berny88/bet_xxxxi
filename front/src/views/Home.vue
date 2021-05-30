<script>
import Sign from '../components/sign.vue'

export default {
	name: 'App',
	components: {
		Sign
	}
}
</script>

<template>
  <div class="home">
    Home <br/>
    <div v-if="$store.state.isConnected">
      Connected : goto display home
    </div>
    <div v-else>
      <Sign/>
      <img alt="Vue logo" src="../assets/img/euro2021.jpg">
    </div>
  </div>
</template>
