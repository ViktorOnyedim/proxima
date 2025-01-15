import { create } from "zustand";
import { mountStoreDevtool } from "simple-zustand-devtools";

const useAuthStore = create((set, get) => ({
    allUserData: null,
    loading: false, // keep track of loading state

    // keep track of user related data
    user: () => ({
        user_id: get().allUserData?.user_id || null,
        username: get().allUserData?.username|| null,

    }),

    // set allUserData state
    setUser: (user) => set({
        allUserData: user
    }),

    setLoading: (loading) => set({ loading }),

    isLoggedIn: () => get().allUserData !== null,
}));

if (import.meta.env.DEV) {
    mountStoreDevtool("Store", useAuthStore);
}

export { useAuthStore };