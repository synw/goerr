<template>
  <div v-html="content"></div>
</template>

<script setup lang="ts">
import hljs from 'highlight.js/lib/core';
import { computed } from 'vue';
import MarkdownIt from 'markdown-it';

const props = defineProps({
  source: {
    type: String,
    required: true,
  },
  hljs: {
    type: Object as () => typeof hljs,
    required: true
  }
});
const md = new MarkdownIt({
  html: true,
  highlight: function (str, lang) {
    if (lang && props.hljs.getLanguage(lang)) {

      try {
        return hljs.highlight(str, { language: lang }).value;
      } catch (e) {
        throw new Error(`Code parse error ${e}`)
      }
    }
    return ''; // use external default escaping
  }
})

const content = computed(() => {
  const src = props.source
  let res = md?.render(src)
  return res
})
</script>

<style lang="sass">
  h1
    @apply text-4xl mb-3
  h2
    @apply text-3xl mt-5 mb-3
  h3
    @apply text-2xl mt-5 mb-3
  h4
    @apply text-xl mt-5 mb-3
  h5
    @apply text-lg mt-5 mb-3
  p
    @apply mb-3 mt-3
</style>