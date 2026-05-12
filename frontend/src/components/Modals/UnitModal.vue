<template>
  <Dialog v-model="show" :options="{ size: 'xl' }">
    <template #body>
      <div class="px-4 pt-5 pb-6 bg-surface-modal sm:px-6">
        <div class="flex items-center justify-between mb-5">
          <div>
            <h3 class="text-2xl font-semibold leading-6 text-ink-gray-9">
              {{ __('New Unit') }}
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
            type="link"
            doctype="Real Estate Project"
            :label="__('Project')"
            v-model="unit.doc.project"
            :required="true"
          />
          <FormControl
            :label="__('Unit Number')"
            v-model="unit.doc.unit_number"
            :required="true"
          />
          <FormControl
            :label="__('Serial Number')"
            v-model="unit.doc.serial_number"
            :required="true"
          />
          <FormControl
            type="link"
            doctype="Real Estate Unit Type"
            :label="__('Unit Type')"
            v-model="unit.doc.unit_type"
            :required="true"
          />
          <FormControl
            type="number"
            :label="__('Area (sqm)')"
            v-model="unit.doc.area"
          />
          <FormControl
            type="currency"
            :label="__('Price')"
            v-model="unit.doc.price"
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
            @click="createUnit"
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

const { document: unit } = useDocument('Real Estate Unit')
const { capture } = useTelemetry()

async function createUnit() {
  if (!unit.doc.project || !unit.doc.unit_number || !unit.doc.serial_number || !unit.doc.unit_type) {
    error.value = 'Project, Unit Number, Serial Number, and Unit Type are required'
    return
  }

  loading.value = true
  error.value = null

  try {
    const doc = await call('frappe.client.insert', {
      doc: {
        doctype: 'Real Estate Unit',
        ...unit.doc,
      },
    })
    loading.value = false
    if (doc.name) {
      capture('unit_created')
      router.push({
        name: 'Unit',
        params: { unitId: doc.name },
      })
      show.value = false
    }
  } catch (err) {
    error.value = err.message || err
    loading.value = false
  }
}
</script>
