// ./components/Header.vue
<script>
export default {
	name: 'NavLink',
	props: ['url', 'text']
}
</script>

<template>
	<a :href="url">{{ text }}</a>
</template>