<template>
  <view class="container">
    <view class="main">
      <text-input
        :on-add='_onPress'
      />
    </view>
  </view>
</template>

<script>
  import TextInput from './src/TodoInput';
  export default {
    components: {
      TextInput
    },
    methods: {
      _onPress : (text) => {
        console.log(text);
      },
    }
  }
</script>

<style>
.container {
  background-color: #da6928;
  flex: 1;
  padding-top: 40px;
  align-items: center;
}
.main {
  flex: 1;
  max-width: 400px;
  align-items: center;
}
</style>