<template>
  <Dialog v-model="show" :options="{ size: 'xl' }">
    <template #body>
      <div class="px-4 pt-5 pb-6 bg-surface-modal sm:px-6">
        <div class="flex items-center justify-between mb-5">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __('New Project') }}
            </h3>
          </div>
          <div class="flex items-center gap-1">
            <Button
              variant="ghost"
              class="w-7"
              icon="x"
              @click="show = false"
            />
          </div>
        </div>
        <div class="flex flex-col gap-4">
          <FormControl
            :label="__('Project Name')"
            v-model="project.doc.project_name"
            :required="true"
          />
          <FormControl
            :label="__('Location')"
            v-model="project.doc.location"
          />
        </div>
        <ErrorMessage v-if="error" class="mt-8" :message="__(error)" />
      </div>
      <div class="px-4 pt-4 pb-7 sm:px-6">
        <div class="space-y-2">
          <Button
            class="w-full"
            variant="solid"
            :label="__('Create')"
            :loading="loading"
            @click="createProject"
          />
        </div>
      </div>
    </template>
  </Dialog>
</template>

<script setup>
import { useDocument } from '@/data/document'
import { useTelemetry } from 'frappe-ui/frappe'
import { call } from 'frappe-ui'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const show = defineModel({ type: Boolean })

const loading = ref(false)
const error = ref(null)

const { document: project } = useDocument('Real Estate Project')
const { capture } = useTelemetry()

async function createProject() {
  if (!project.doc.project_name) {
    error.value = 'Project Name is required'
    return
  }

  loading.value = true
  error.value = null

  try {
    const doc = await call('frappe.client.insert', {
      doc: {
        doctype: 'Real Estate Project',
        ...project.doc,
      },
    })
    loading.value = false
    if (doc.name) {
      capture('project_created')
      router.push({
        name: 'Project',
        params: { projectId: doc.name },
      })
      show.value = false
    }
  } catch (err) {
    error.value = err.message || err
    loading.value = false
  }
}
</script>
