<template>
  <div v-if="isReady">
    <render-md :source="code" :hljs="hljs"></render-md>
  </div>
</template>

<script setup lang="ts">
import RenderMd from '@/widgets/RenderMd.vue';
import { api } from "@/state";
import { ref, watchEffect } from "vue";
import "highlight.js/styles/stackoverflow-light.css";
import python from 'highlight.js/lib/languages/python';
import hljs from 'highlight.js/lib/core';
hljs.registerLanguage('python', python);

const props = defineProps({
  fileUrl: {
    type: String,
    required: true
  }
})

const code = ref("");
const isReady = ref(false);

async function load() {
  isReady.value = false;
  code.value = await api.get<string>(props.fileUrl);
  isReady.value = true;
}

watchEffect(() => load())
</script>