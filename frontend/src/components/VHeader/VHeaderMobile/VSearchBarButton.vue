<template>
  <VOldIconButton
    class="border-tx bg-tx"
    :label="label"
    :button-props="{ variant: 'plain--avoid' }"
    v-on="$listeners"
  >
    <template #default="{ iconSize }">
      <span
        class="relative flex flex-shrink-0 flex-grow-0 items-center justify-center rounded-sm group-focus-visible/button:ring group-focus-visible/button:ring-pink group-active/button:ring group-active/button:ring-pink"
        :class="[`h-${innerSize} w-${innerSize}`, innerAreaClasses]"
      >
        <VIcon
          :name="icon"
          :rtl-flip="rtlFlip"
          class="pointer-events-none"
          :size="iconSize"
        />
        <!--  @slot The element that can show a notification label for the button, can be absolutely positioned  -->
        <slot name="notification" />
      </span>
    </template>
  </VOldIconButton>
</template>
<script lang="ts">
import { defineComponent, PropType } from "vue"

import VIcon from "~/components/VIcon/VIcon.vue"
import VOldIconButton from "~/components/VIconButton/VOldIconButton.vue"

import type { TranslateResult } from "vue-i18n"

/**
 * The buttons placed inside the mobile search bar in the header.
 * They are based on the VOldIconButton, look like they have a smallish focus area
 * (32x32px), but actually have a larger tappable area of 48x48px to comply with
 * accessibility requirements.
 */
export default defineComponent({
  name: "VSearchBarButton",
  components: { VIcon, VOldIconButton },
  props: {
    /**
     * The path for the icon.
     */
    icon: {
      type: String,
      required: true,
    },
    /**
     * The size of the inner area that has a different color,
     * sometimes only when interactive.
     */
    innerSize: {
      type: Number as PropType<6 | 8>,
      default: 8,
    },
    /**
     * The classes to apply to the inner area for styling resting/hover states.
     */
    innerAreaClasses: {
      type: String,
      default: "",
    },
    /**
     * Whether the icon should be flipped when the page is in RTL mode.
     */
    rtlFlip: {
      type: Boolean,
      default: false,
    },
    /**
     * The label to use as accessible name for the button (aria-label).
     */
    label: {
      type: [String, Object] as PropType<string | TranslateResult>,
      required: true,
    },
  },
})
</script>
