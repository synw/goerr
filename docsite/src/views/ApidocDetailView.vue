<template>
  <div class="container p-3 mx-auto">
    <render-md-file-python :file-url="`/apidoc/${file}.md`"></render-md-file-python>
  </div>
</template>

<script setup lang="ts">
import { ref, watchEffect } from 'vue';
import RenderMdFilePython from '@/widgets/RenderMdFilePython.vue';
import router from '@/router';

const file = ref("")

watchEffect(() => {
  file.value = router.currentRoute.value.params?.file.toString() ?? ""
})
</script>

