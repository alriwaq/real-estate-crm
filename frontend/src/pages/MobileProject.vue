<template>
  <LayoutHeader v-if="doc.name">
    <header
      class="relative flex h-10.5 items-center justify-between gap-2 py-2.5 pl-2"
    >
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </header>
  </LayoutHeader>
  <div v-if="doc.name" class="flex flex-col h-full overflow-hidden">
    <div class="flex flex-col gap-2 border-b p-4">
      <div class="truncate text-lg font-medium text-ink-gray-9">
        {{ title }}
      </div>
      <div class="flex gap-1.5">
        <Button
          v-if="canDelete"
          :label="__('Delete')"
          theme="red"
          size="sm"
          iconLeft="trash-2"
          @click="deleteProject"
        />
      </div>
    </div>
    <Tabs
      v-model="tabIndex"
      as="div"
      :tabs="tabs"
      class="flex flex-1 overflow-auto flex-col [&_[role='tablist']]:gap-7.5 [&_[role='tablist']]:px-4 [&_[role='tabpanel']:not([hidden])]:flex [&_[role='tabpanel']:not([hidden])]:grow"
    >
      <template #tab-panel="{ tab }">
        <div v-if="tab.name === 'Details'" class="flex flex-1 flex-col overflow-hidden">
          <div
            v-if="sections.data"
            class="flex flex-1 flex-col justify-between overflow-hidden"
          >
            <SidePanelLayout
              :sections="sections.data"
              doctype="Real Estate Project"
              :docname="doc.name"
              @reload="sections.reload"
            />
          </div>
        </div>
        <Activities
          v-else
          ref="activities"
          v-model:reload="reload"
          v-model:tabIndex="tabIndex"
          doctype="Real Estate Project"
          :docname="projectId"
          :tabs="tabs"
          @afterSave="() => {}"
        />
      </template>
    </Tabs>
  </div>
  <DeleteLinkedDocModal
    v-if="showDeleteLinkedDocModal"
    v-model="showDeleteLinkedDocModal"
    :doctype="'Real Estate Project'"
    :docname="projectId"
    name="Projects"
  />
</template>

<script setup>
import DeleteLinkedDocModal from '@/components/DeleteLinkedDocModal.vue'
import SidePanelLayout from '@/components/SidePanelLayout.vue'
import Icon from '@/components/Icon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import DetailsIcon from '@/components/Icons/DetailsIcon.vue'
import ActivityIcon from '@/components/Icons/ActivityIcon.vue'
import TaskIcon from '@/components/Icons/TaskIcon.vue'
import NoteIcon from '@/components/Icons/NoteIcon.vue'
import AttachmentIcon from '@/components/Icons/AttachmentIcon.vue'
import Activities from '@/components/Activities/Activities.vue'
import { useDocument } from '@/data/document'
import { getSettings } from '@/stores/settings'
import { getMeta } from '@/stores/meta'
import { getView } from '@/utils/view'
import {
  Breadcrumbs,
  Tabs,
  createResource,
  usePageMeta,
} from 'frappe-ui'
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  projectId: { type: String, required: true },
})

const { brand } = getSettings()
const { doctypeMeta } = getMeta('Real Estate Project')

const route = useRoute()

const { document, permissions } = useDocument(
  'Real Estate Project',
  props.projectId,
)

const canDelete = computed(() => permissions.data?.permissions?.delete || false)
const doc = computed(() => document.doc || {})

const reload = ref(false)
const activities = ref(null)
const showDeleteLinkedDocModal = ref(false)

const breadcrumbs = computed(() => {
  let items = [{ label: __('Projects'), route: { name: 'Projects' } }]

  if (route.query.view || route.query.viewType) {
    let view = getView(
      route.query.view,
      route.query.viewType,
      'Real Estate Project',
    )
    if (view) {
      items.push({
        label: __(view.label),
        icon: view.icon,
        route: {
          name: 'Projects',
          params: { viewType: route.query.viewType },
          query: { view: route.query.view },
        },
      })
    }
  }

  items.push({
    label: title.value,
    route: { name: 'Project', params: { projectId: props.projectId } },
  })
  return items
})

const title = computed(() => {
  let t = doctypeMeta.value?.title_field || 'name'
  return doc.value?.[t] || props.projectId
})

usePageMeta(() => {
  return { title: title.value, icon: brand.favicon }
})

const tabIndex = ref(0)
const tabs = [
  { name: 'Details', label: __('Details'), icon: DetailsIcon },
  { name: 'Activity', label: __('Activity'), icon: ActivityIcon },
  { name: 'Tasks', label: __('Tasks'), icon: TaskIcon },
  { name: 'Notes', label: __('Notes'), icon: NoteIcon },
  { name: 'Attachments', label: __('Attachments'), icon: AttachmentIcon },
]

const sections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_sidepanel_sections',
  cache: ['sidePanelSections', 'Real Estate Project'],
  params: { doctype: 'Real Estate Project' },
  auto: true,
})

function deleteProject() {
  showDeleteLinkedDocModal.value = true
}
</script>
