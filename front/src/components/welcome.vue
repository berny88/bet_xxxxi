<script>
export default {
	name: 'Welcome'
}
</script>
<template>
        <div class="container grid-xs">

            <h1><center>Welcome</center></h1>

            <div class="col-xs-12">
            <router-link :to="{ name: 'User', params: { uid: $store.state.uid }}" 
                class="btn btn-link">Your settings</router-link>
                

            </div>
        </div>
</template>