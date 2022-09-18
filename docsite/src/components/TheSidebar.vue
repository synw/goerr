<template>
  <div>
    <div>
      <div class="mt-3 text-xl">Api doc</div>
      <apidocs-list class="mt-3"></apidocs-list>
    </div>
    <div>
      <div class="mt-5 text-xl">Examples</div>
      <examples-list class="mt-3"></examples-list>
    </div>
  </div>
</template>

<script setup lang="ts">
import ApidocsList from "@/components/ApidocsList.vue";
import ExamplesList from "@/components/ExamplesList.vue";
</script>