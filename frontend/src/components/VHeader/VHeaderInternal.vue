<template>
  <header
    ref="nodeRef"
    class="main-header z-30 flex h-20 w-full items-stretch justify-between gap-x-2 border-b border-tx px-2 py-4 md:py-4 lg:pe-10 lg:ps-6"
  >
    <VHomeLink variant="dark" />
    <nav class="hidden lg:flex">
      <VPageLinks
        mode="light"
        class="flex items-center gap-6 text-sm"
        @close="closePageMenu"
      />
    </nav>
    <div class="flex lg:hidden">
      <VOldIconButton
        id="menu-button"
        ref="menuButtonRef"
        :icon-props="{ name: 'menu' }"
        :label="$t('header.aria.menu')"
        v-bind="triggerA11yProps"
        class="border-tx hover:bg-dark-charcoal hover:text-white"
        :class="{ 'bg-dark-charcoal text-white': isModalVisible }"
        @click="onTriggerClick"
      />
      <template v-if="triggerElement">
        <VPopoverContent
          v-if="isSm"
          z-index="popover"
          :hide="closePageMenu"
          :visible="isModalVisible"
          :trigger-element="triggerElement"
          :trap-focus="false"
          aria-labelledby="menu-button"
        >
          <VPageLinks
            mode="dark"
            variant="itemgroup"
            class="label-regular w-50 items-start"
            @close="closePageMenu"
          />
        </VPopoverContent>
        <VModalContent
          v-else-if="!isSm"
          ref="modalContentRef"
          aria-labelledby="menu-button"
          :hide="closePageMenu"
          variant="full"
          mode="dark"
          modal-content-classes="flex sm:hidden"
          :visible="isModalVisible"
          @open="openPageMenu"
        >
          <template #top-bar>
            <div class="flex h-20 w-full justify-between px-2 py-4">
              <VHomeLink variant="light" />
              <VCloseButton
                variant="black"
                icon-size="medium"
                :label="$t('modal.closePagesMenu')"
                @close="closePageMenu"
              />
            </div>
          </template>
          <template #default>
            <nav>
              <VPageLinks
                mode="dark"
                class="mt-3 flex flex-col items-end gap-y-6"
                nav-link-classes="text-white text-3xl focus-visible:ring-yellow"
                :is-in-modal="true"
                @close="closePageMenu"
              />
            </nav>
            <VWordPressLink
              class="mt-auto focus-visible:ring-yellow focus-visible:ring-offset-0"
              mode="dark"
            />
          </template>
        </VModalContent>
      </template>
    </div>
  </header>
</template>

<script lang="ts">
import { computed, defineComponent, ref, watch } from "vue"
import { useRoute } from "@nuxtjs/composition-api"

import { useDialogControl } from "~/composables/use-dialog-control"
import { useAnalytics } from "~/composables/use-analytics"
import usePages from "~/composables/use-pages"

import { useUiStore } from "~/stores/ui"

import VCloseButton from "~/components/VCloseButton.vue"
import VHomeLink from "~/components/VHeader/VHomeLink.vue"
import VOldIconButton from "~/components/VIconButton/VOldIconButton.vue"
import VPageLinks from "~/components/VHeader/VPageLinks.vue"
import VModalContent from "~/components/VModal/VModalContent.vue"
import VPopoverContent from "~/components/VPopover/VPopoverContent.vue"
import VWordPressLink from "~/components/VHeader/VWordPressLink.vue"

export default defineComponent({
  name: "VHeaderInternal",
  components: {
    VCloseButton,
    VModalContent,
    VPopoverContent,
    VHomeLink,
    VOldIconButton,
    VPageLinks,
    VWordPressLink,
  },
  setup(_, { emit }) {
    const menuButtonRef = ref<InstanceType<typeof VOldIconButton> | null>(null)
    const nodeRef = ref<HTMLElement | null>(null)
    const modalContentRef = ref<InstanceType<typeof VModalContent> | null>(null)

    const uiStore = useUiStore()

    const route = useRoute()

    const { sendCustomEvent } = useAnalytics()

    const { all: allPages, current: currentPage } = usePages()

    const isModalVisible = ref(false)

    const isSm = computed(() => uiStore.isBreakpoint("sm"))

    const triggerElement = computed(
      () => (menuButtonRef.value?.$el as HTMLElement) || null
    )

    const lockBodyScroll = computed(() => !isSm.value)

    const deactivateFocusTrap = computed(
      () => modalContentRef.value?.deactivateFocusTrap
    )

    const {
      close: closePageMenu,
      open: openPageMenu,
      onTriggerClick,
      triggerA11yProps,
    } = useDialogControl({
      visibleRef: isModalVisible,
      nodeRef,
      lockBodyScroll,
      emit,
      deactivateFocusTrap,
    })

    const eventedOnTriggerClick = () => {
      if (!isModalVisible.value) {
        sendCustomEvent("OPEN_PAGES_MENU", {})
      }
      return onTriggerClick()
    }

    // When clicking on an internal link in the modal, close the modal
    watch(route, () => {
      if (isModalVisible.value) {
        closePageMenu()
      }
    })

    return {
      menuButtonRef,
      modalContentRef,
      nodeRef,

      allPages,
      currentPage,

      isModalVisible,
      closePageMenu,
      openPageMenu,
      isSm,
      onTriggerClick: eventedOnTriggerClick,
      triggerA11yProps,
      triggerElement,
    }
  },
})
</script>
