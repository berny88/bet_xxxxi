<script>
import Sign from '../components/sign.vue'
import Welcome from '../components/welcome.vue'

export default {
	name: 'App',
	components: {
		Sign,
    Welcome
	}
}
</script>

<template>
  <div class="home">
    <div v-if="$store.state.isConnected">
      You are now connected.<br/>
      <Welcome/>
    </div>
    <div v-else>
      You must sign.<br/>
      <Sign/>
      <img alt="Vue logo" src="../assets/img/euro2021.jpg">
    </div>
  </div>
</template>
