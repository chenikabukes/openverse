<template>
  <div
    id="safety-wall"
    class="relative flex h-full w-full flex-grow items-center justify-center border-t border-dark-charcoal-20 bg-white py-8 text-center"
  >
    <section class="mx-auto max-w-2xl px-8 text-sm leading-relaxed">
      <h1 class="heading-5 mb-2">
        {{ $t("sensitiveContent.singleResult.title") }}
      </h1>
      <p class="mb-2">
        {{ $t("sensitiveContent.singleResult.explanation") }}
      </p>
      <p v-for="reason in media.sensitivity" :key="reason">
        {{
          $t(`sensitiveContent.reasons.${camel(reason)}`, {
            openverse: "Openverse",
          })
        }}
      </p>
      <i18n tag="p" class="mt-2" path="sensitiveContent.singleResult.learnMore">
        <template #openverse>Openverse</template>
        <template #link>
          <VLink class="text-pink hover:underline" href="/sensitive-content">{{
            $t("sensitiveContent.singleResult.link")
          }}</VLink>
          {{ " " }}
        </template>
      </i18n>

      <div
        class="mt-6 flex flex-col items-stretch justify-center gap-4 md:flex-row md:gap-6"
      >
        <VButton
          as="VLink"
          size="large"
          variant="filled-dark"
          class="label-bold"
          :href="backToSearchPath || '/'"
        >
          {{ $t("singleResult.back") }}
        </VButton>
        <VButton
          size="large"
          variant="bordered-gray"
          class="label-bold"
          has-icon-end
          @click="showMedia"
        >
          {{ $t("sensitiveContent.singleResult.show") }}
          <VIcon name="eye-open" />
        </VButton>
      </div>
    </section>
  </div>
</template>

<script lang="ts">
import { PropType, computed, defineComponent } from "@nuxtjs/composition-api"
import { camel } from "case"

import { useSearchStore } from "~/stores/search"
import type { AudioDetail, ImageDetail } from "~/types/media"

import VLink from "~/components/VLink.vue"
import VButton from "~/components/VButton.vue"
import VIcon from "~/components/VIcon/VIcon.vue"

export default defineComponent({
  name: "VSafetyWall",
  components: {
    VButton,
    VIcon,
    VLink,
  },
  props: {
    media: {
      type: Object as PropType<AudioDetail | ImageDetail>,
      required: true,
    },
  },
  setup(_, { emit }) {
    const searchStore = useSearchStore()
    const backToSearchPath = computed(() => searchStore.backToSearchPath)

    const showMedia = () => {
      emit("reveal")
    }

    return {
      backToSearchPath,
      showMedia,
      camel,
    }
  },
})
</script>

<style scoped>
#safety-wall {
  background: no-repeat url(~/assets/safety-bg.png);
  background-size: 100% 100%;
}
</style>
