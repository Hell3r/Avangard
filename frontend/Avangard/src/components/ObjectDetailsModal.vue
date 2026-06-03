<template>
  <div
    v-if="open"
    class="fixed inset-0 bg-black/30 flex items-center justify-center p-4"
    @click.self="close"
  >
    <div class="bg-white rounded-2xl shadow-lg w-full max-w-3xl p-5">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h3 class="text-xl font-bold">Информация об объекте</h3>
          <div class="mt-1 text-sm text-gray-500">{{ addressName }} (ID: {{ addressId }})</div>
        </div>
        <button class="text-gray-500 hover:text-gray-800" @click="close">✕</button>
      </div>

      <div class="mt-5 grid grid-cols-12 gap-4">
        <div class="col-span-6">
          <div class="border rounded-2xl p-4">
            <div class="flex items-center justify-between">
              <div class="font-semibold">Мастер</div>
              <div class="text-sm text-[#1F5D3A] font-semibold">{{ master?.full_name ?? '—' }}</div>
            </div>

            <div class="mt-3 text-sm text-gray-600">
              <div><b>Контакты:</b> {{ master?.username ?? '—' }}</div>
              <div><b>Роль:</b> {{ master?.role ?? '—' }}</div>
            </div>

            <div class="mt-4">
              <div class="text-sm font-semibold mb-2">Привязка адреса мастеру</div>
              <div class="space-y-2">
                <input
                  v-model="masterUsername"
                  placeholder="ФИО мастера"
                  class="w-full border rounded-xl px-3 py-2 outline-none focus:ring-2 focus:ring-[#1F5D3A]/30"
                />

                <button
                  class="w-full bg-[#1F5D3A] hover:bg-[#17482D] text-white px-4 py-2 rounded-xl disabled:opacity-60"
                  :disabled="saving"
                  @click="bindAddressToMaster"
                >
                  {{ saving ? 'Привязка...' : 'Привязать' }}
                </button>

                <div v-if="bindError" class="text-sm text-red-600">{{ bindError }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-span-6">
          <div class="border rounded-2xl p-4">
            <div class="flex items-center justify-between">
              <div class="font-semibold">Сотрудники объекта</div>
              <div class="text-sm text-gray-500">Всего: {{ totalEmployees }}</div>
            </div>

            <div class="mt-3 grid grid-cols-2 gap-3">
              <div class="rounded-2xl border p-3">
                <div class="text-sm text-gray-500">Присутствуют</div>
                <div class="text-lg font-bold text-green-700">{{ presentEmployees.length }}</div>
              </div>
              <div class="rounded-2xl border p-3">
                <div class="text-sm text-gray-500">Отсутствуют</div>
                <div class="text-lg font-bold text-red-600">{{ absentEmployees.length }}</div>
              </div>
            </div>

            <div class="mt-4 space-y-3">
              <div>
                <div class="text-sm font-semibold text-gray-700 mb-2">Список присутствующих</div>
                <div class="space-y-2">
                  <div
                    v-for="u in presentEmployees"
                    :key="u.id"
                    class="border rounded-xl p-3 bg-green-50"
                  >
                    <div class="font-semibold">{{ u.full_name ?? '—' }}</div>
                    <div class="text-xs text-gray-600">{{ formatDateTime(u.on_site_since) }}</div>
                  </div>
                  <div v-if="!presentEmployees.length" class="text-sm text-gray-500">Пока никого</div>
                </div>
              </div>

              <div>
                <div class="text-sm font-semibold text-gray-700 mb-2">Список отсутствующих</div>
                <div class="space-y-2">
                  <div
                    v-for="u in absentEmployees"
                    :key="u.id"
                    class="border rounded-xl p-3 bg-red-50"
                  >
                    <div class="font-semibold">{{ u.full_name ?? '—' }}</div>
                    <div class="text-xs text-gray-600">Нет на объекте</div>
                  </div>
                  <div v-if="!absentEmployees.length" class="text-sm text-gray-500">Пока никого</div>
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'

type AddressRow = { id: number; name: string }

type Master = {
  id: number
  username: string
  full_name?: string | null
  role?: string
  address_id?: number | null
}

type UserOnSite = {
  id: number
  username: string
  full_name?: string | null
  is_on_site?: boolean
  on_site_since?: string | null
  role?: string
}

type UserOffSite = {
  id: number
  username: string
  full_name?: string | null
  role?: string
}

const open = ref(false)
const addressId = ref<number>(0)
const addressName = ref<string>('')

const master = ref<Master | null>(null)

const saving = ref(false)
const bindError = ref<string | null>(null)
const masterUsername = ref('')

const employees = ref<UserOnSite[]>([])
const allEmployees = ref<(UserOnSite | UserOffSite)[]>([])

const totalEmployees = computed(() => allEmployees.value.length)
const presentEmployees = computed(() => employees.value)
const absentEmployees = computed(() => {
  const presentIds = new Set(employees.value.map((u) => u.id))
  return allEmployees.value.filter((u) => !presentIds.has(u.id)) as UserOffSite[]
})

function openModal(addr: AddressRow) {
  open.value = true
  addressId.value = addr.id
  addressName.value = addr.name

  // Заглушка: грузим в UI-версии только присутствующих через доступный master-endpoint.
  void loadEmployees()
  void loadMasterInfo()
}

function close() {
  open.value = false
}

async function loadEmployees() {
  // Чтобы не плодить API-слой сейчас, используем тот endpoint, что уже есть:
  // /v1/users/on-site
  // Важно: сервер фильтрует по address_id текущего master (в бэке), поэтому для админа это может быть некорректно.
  // Здесь это всё равно частично полезно для UI.
  try {
    const token = localStorage.getItem('access_token')
    const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

    // Для админа нужен отдельный endpoint, иначе сервер отфильтрует по address мастера и вернёт пусто.
    const isAdmin = (() => {
      const raw = localStorage.getItem('user_info')
      if (!raw) return false
      try {
        const parsed = JSON.parse(raw)
        return parsed?.role === 'admin'
      } catch {
        return false
      }
    })()

    const url = isAdmin
      ? `http://0.0.0.0:8000/v1/users/on-site/all?skip=0&limit=200`
      : `http://0.0.0.0:8000/v1/users/on-site?skip=0&limit=200`

    const res = await fetch(url, { headers })
    if (!res.ok) return

    // сервер возвращает только on-site; absent вычислим ниже через allEmployees, если удастся получить полный список.
    employees.value = (await res.json()) as UserOnSite[]

    // Если admin endpoint возвращает полный список активных, можно так же использовать его для absent.
    allEmployees.value = employees.value
  } catch {
    // ignore
  }
}

async function loadMasterInfo() {
  const tokenUser = (() => {
    const raw = localStorage.getItem('user_info')
    if (!raw) return null
    try {
      return JSON.parse(raw) as {
        role?: string
        address_id?: number
        user_id?: number
        username?: string
        full_name?: string
      }
    } catch {
      return null
    }
  })()

  if (tokenUser?.role === 'master' && tokenUser?.address_id === addressId.value) {
    const userId = tokenUser.user_id
    const username = tokenUser.username

    master.value = {
      id: userId ?? -1,
      username: username ?? '',
      full_name: tokenUser.full_name,
      role: tokenUser.role,
      address_id: tokenUser.address_id
    }
  } else {
    master.value = null
  }
}

async function bindAddressToMaster() {
  bindError.value = null
  saving.value = true

  try {
    const token = localStorage.getItem('access_token')
    const headers: Record<string, string> = token ? { Authorization: `Bearer ${token}` } : {}

    const url = `http://0.0.0.0:8000/v1/users/master/bind-address?address_id=${encodeURIComponent(String(addressId.value))}&master_full_name=${encodeURIComponent(String(masterUsername.value.trim()))}`


    const res = await fetch(url, {
      method: 'PUT',
      headers
    })

    if (!res.ok) {
      const text = await res.text().catch(() => '')
      throw new Error(`Ошибка привязки: ${res.status} ${text}`)
    }

    await loadMasterInfo()
  } catch (e) {
    bindError.value = e instanceof Error ? e.message : String(e)
  } finally {
    saving.value = false
  }
}


function formatDateTime(iso?: string | null) {
  if (!iso) return '—'
  try {
    return new Date(iso).toLocaleString('ru-RU')
  } catch {
    return iso
  }
}

defineExpose({ openModal })
</script>

