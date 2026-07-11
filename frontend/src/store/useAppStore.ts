import { create } from 'zustand'

interface AppState {
  isSidebarOpen: boolean
  toggleSidebar: () => void
  activeAssetId: string | null
  setActiveAssetId: (id: string | null) => void
}

export const useAppStore = create<AppState>((set) => ({
  isSidebarOpen: true,
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  
  activeAssetId: null,
  setActiveAssetId: (id) => set({ activeAssetId: id }),
}))
