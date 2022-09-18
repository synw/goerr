<template>
  <div class="container mx-auto">
    <div class="p-5" v-if="isReady">
      <py-code-block id="script" :py="py" :code="code"></py-code-block>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, ref } from 'vue';
import { PyCodeBlock } from "vuepython";
import "vuepython/style.css";
import "highlight.js/styles/stackoverflow-light.css"
import { py, api } from '@/state';
import router from "@/router";
import { onBeforeRouteUpdate } from 'vue-router';
import { examplesExtension } from '@/conf';

const code = ref("");
const isReady = ref(false);

async function load() {
  isReady.value = false;
  const file = router.currentRoute.value.params?.file.toString() ?? "";
  code.value = await api.get<string>(`/examples/${file + examplesExtension}`);
  isReady.value = true;
}

onBeforeMount(() => load());
onBeforeRouteUpdate(() => load())
</script>