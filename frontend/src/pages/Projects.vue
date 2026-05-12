<template>
  <div class="flex flex-col h-full bg-gray-50">
    <!-- Header -->
    <div class="flex items-center justify-between px-6 py-4 border-b bg-white">
      <div class="flex items-center gap-4">
        <button
          @click="goBack"
          class="text-gray-600 hover:text-gray-900 text-2xl"
        >
          ← Back
        </button>
        <div>
          <h1 class="text-2xl font-bold text-gray-900">{{ isNew ? 'New Product' : productData.product_name }}</h1>
          <p class="text-sm text-gray-600 mt-1">{{ isNew ? 'Create a new product' : `Code: ${productData.product_code}` }}</p>
        </div>
      </div>
      <div class="flex gap-3">
        <button
          @click="saveProduct"
          :disabled="saving"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition"
        >
          {{ saving ? 'Saving...' : 'Save' }}
        </button>
        <button
          v-if="!isNew"
          @click="deleteCurrentProduct"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition"
        >
          Delete
        </button>
      </div>
    </div>

    <!-- Form Content -->
    <div class="flex-1 overflow-auto">
      <div class="max-w-4xl mx-auto p-6 space-y-6">
        <!-- Basic Information Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Product Code *</label>
              <input
                v-model="productData.product_code"
                type="text"
                :disabled="!isNew"
                placeholder="Enter product code"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Product Name</label>
              <input
                v-model="productData.product_name"
                type="text"
                placeholder="Enter product name"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>
        </div>

        <!-- Pricing Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Pricing</h2>
          <div class="grid grid-cols-2 gap-6">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Standard Selling Rate</label>
              <input
                v-model="productData.standard_rate"
                type="number"
                step="0.01"
                placeholder="0.00"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div class="flex items-end">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  v-model="productData.disabled"
                  type="checkbox"
                  class="w-4 h-4 border border-gray-300 rounded focus:ring-2 focus:ring-blue-500"
                />
                <span class="text-sm font-medium text-gray-700">Disabled</span>
              </label>
            </div>
          </div>
        </div>

        <!-- Image Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Product Image</h2>
          <div class="flex gap-6">
            <div v-if="productData.image" class="flex-shrink-0">
              <img
                :src="productData.image"
                alt="Product Image"
                class="w-32 h-32 object-cover rounded-lg"
              />
            </div>
            <div class="flex-1">
              <label class="block text-sm font-medium text-gray-700 mb-2">Upload Image</label>
              <input
                type="file"
                accept="image/*"
                @change="handleImageUpload"
                class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <p class="text-xs text-gray-500 mt-2">Supported formats: JPG, PNG, GIF. Max size: 5MB</p>
            </div>
          </div>
        </div>

        <!-- Description Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">Description</h2>
          <textarea
            v-model="productData.description"
            placeholder="Enter product description"
            rows="6"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

const productData = ref({
  product_code: '',
  product_name: '',
  standard_rate: 0,
  disabled: false,
  image: '',
  description: ''
})

const saving = ref(false)
const loading = ref(false)

const isNew = computed(() => route.params.productId === 'new')

const loadProduct = async () => {
  if (isNew.value) return

  loading.value = true
  try {
    const response = await frappe.call({
      method: 'frappe.client.get',
      args: {
        doctype: 'CRM Product',
        name: route.params.productId
      }
    })
    if (response.message) {
      productData.value = {
        product_code: response.message.product_code || '',
        product_name: response.message.product_name || '',
        standard_rate: response.message.standard_rate || 0,
        disabled: response.message.disabled || false,
        image: response.message.image || '',
        description: response.message.description || ''
      }
    }
  } catch (error) {
    console.error('Error loading product:', error)
    frappe.msgprint('Error loading product')
  } finally {
    loading.value = false
  }
}

const saveProduct = async () => {
  if (!productData.value.product_code) {
    frappe.msgprint('Product Code is required')
    return
  }

  saving.value = true
  try {
    const method = isNew.value ? 'frappe.client.insert' : 'frappe.client.set_value'
    const args = isNew.value
      ? {
          doc: {
            doctype: 'CRM Product',
            ...productData.value
          }
        }
      : {
          doctype: 'CRM Product',
          name: route.params.productId,
          fieldname: productData.value
        }

    const response = await frappe.call({
      method,
      args
    })

    if (response.message) {
      frappe.msgprint('Product saved successfully')
      if (isNew.value) {
        router.push(`/products/${response.message.name}`)
      }
    }
  } catch (error) {
    console.error('Error saving product:', error)
    frappe.msgprint('Error saving product')
  } finally {
    saving.value = false
  }
}

const deleteCurrentProduct = async () => {
  if (confirm('Are you sure you want to delete this product?')) {
    try {
      await frappe.call({
        method: 'frappe.client.delete',
        args: {
          doctype: 'CRM Product',
          name: route.params.productId
        }
      })
      frappe.msgprint('Product deleted successfully')
      router.push('/products')
    } catch (error) {
      console.error('Error deleting product:', error)
      frappe.msgprint('Error deleting product')
    }
  }
}

const handleImageUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)
  formData.append('doctype', 'CRM Product')
  formData.append('docname', isNew.value ? '' : route.params.productId)
  formData.append('fieldname', 'image')

  try {
    const response = await fetch('/api/method/frappe.client.upload', {
      method: 'POST',
      body: formData
    })
    const data = await response.json()
    if (data.message) {
      productData.value.image = data.message.file_url
      frappe.msgprint('Image uploaded successfully')
    }
  } catch (error) {
    console.error('Error uploading image:', error)
    frappe.msgprint('Error uploading image')
  }
}

const goBack = () => {
  router.push('/products')
}

onMounted(() => {
  if (!isNew.value) {
    loadProduct()
  }
})
</script>

<style scoped>
/* Add any component-specific styles here */
</style>
