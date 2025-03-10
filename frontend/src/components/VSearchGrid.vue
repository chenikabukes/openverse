<template>
  <section v-if="!showError">
    <header v-if="query.q && supported" class="my-0 md:mb-8 md:mt-4">
      <VSearchResultsTitle :size="isAllView ? 'large' : 'default'">
        {{ searchTerm }}
      </VSearchResultsTitle>
    </header>

    <slot name="media" />

    <VExternalSearchForm
      v-if="!isAllView"
      :has-no-results="hasNoResults"
      :search-term="searchTerm"
      :is-supported="supported"
    />
  </section>
  <VErrorSection v-else class="w-full py-10">
    <template #image>
      <VErrorImage error-code="NO_RESULT" />
    </template>
    <VNoResults :search-term="searchTerm" />
  </VErrorSection>
</template>

<script lang="ts">
import { computed, defineComponent, PropType } from "vue"

import { ALL_MEDIA, SearchType } from "~/constants/media"
import { NO_RESULT } from "~/constants/errors"
import { defineEvent } from "~/types/emits"
import type { FetchState } from "~/types/fetch-state"
import type { ApiQueryParams } from "~/utils/search-query-transform"

import VExternalSearchForm from "~/components/VExternalSearch/VExternalSearchForm.vue"
import VErrorSection from "~/components/VErrorSection/VErrorSection.vue"
import VErrorImage from "~/components/VErrorSection/VErrorImage.vue"
import VNoResults from "~/components/VErrorSection/VNoResults.vue"
import VSearchResultsTitle from "~/components/VSearchResultsTitle.vue"

export default defineComponent({
  name: "VSearchGrid",
  components: {
    VErrorSection,
    VExternalSearchForm,
    VErrorImage,
    VNoResults,
    VSearchResultsTitle,
  },
  props: {
    supported: {
      type: Boolean,
      required: true,
    },
    query: {
      type: Object as PropType<ApiQueryParams>,
      required: true,
    },
    searchType: {
      type: String as PropType<SearchType>,
      required: true,
    },
    fetchState: {
      type: Object as PropType<FetchState>,
      required: true,
    },
    resultsCount: {
      type: Number,
      required: true,
    },
  },
  emits: {
    tab: defineEvent<[KeyboardEvent]>(),
  },
  setup(props) {
    const hasNoResults = computed(() => {
      // noResult is hard-coded for search types that are not currently
      // supported by Openverse built-in search
      return props.supported
        ? Boolean(
            props.query.q !== "" &&
              props.fetchState.hasStarted &&
              props.resultsCount === 0
          )
        : false
    })

    const isAllView = computed(() => props.searchType === ALL_MEDIA)

    const searchTerm = computed(() => props.query.q || "")

    const showError = computed(() => {
      return (
        props.fetchState.hasStarted &&
        !props.fetchState.isFetching &&
        props.resultsCount === 0
      )
    })

    return {
      hasNoResults,
      isAllView,
      NO_RESULT,
      searchTerm,
      showError,
    }
  },
})
</script>
