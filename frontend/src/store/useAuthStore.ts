import { create } from 'zustand'
import { User } from '../types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  login: (user: User) => void
  logout: () => void
}

// Initialize with a mock user for the demo
const mockUser: User = {
  id: "u-1",
  name: "Senior Engineer",
  email: "engineer@industrial.com",
  role: "admin",
  avatarInitials: "EN"
}

export const useAuthStore = create<AuthState>((set) => ({
  user: mockUser,
  isAuthenticated: true,
  login: (user) => set({ user, isAuthenticated: true }),
  logout: () => set({ user: null, isAuthenticated: false }),
}))
