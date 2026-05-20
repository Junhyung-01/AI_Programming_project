import { create } from 'zustand';
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.DEV ? 'http://localhost:8001/api/game' : '/api/game',
});

export interface GameState {
  player: any;
  current_chapter: number;
  current_stage: number;
  in_battle: boolean;
  in_shop: boolean;
  is_boss: boolean;
  enemies: any[];
  logs: string[];
  game_over: boolean;
  game_clear: boolean;
}

interface StoreState {
  gameState: GameState | null;
  gameData: any;
  fetchGameData: () => Promise<void>;
  startGame: (name: string, job_class: string) => Promise<void>;
  fetchState: () => Promise<void>;
  chooseRoute: (route: 'battle' | 'shop' | 'rest') => Promise<void>;
  doAction: (actionType: string, payload?: any) => Promise<void>;
  buyItem: (itemIndex: number) => Promise<void>;
  leaveShop: () => Promise<void>;
}

export const useStore = create<StoreState>((set) => ({
  gameState: null,
  gameData: null,
  
  fetchGameData: async () => {
    const res = await api.get('/data');
    set({ gameData: res.data });
  },

  startGame: async (name, job_class) => {
    const res = await api.post('/start', { name, job_class });
    set({ gameState: res.data });
  },

  fetchState: async () => {
    const res = await api.get('/state');
    set({ gameState: res.data });
  },

  chooseRoute: async (route) => {
    const res = await api.post('/choose_route', { route });
    set({ gameState: res.data });
  },

  doAction: async (actionType, payload = {}) => {
    const reqData = { action_type: actionType, ...payload };
    const res = await api.post('/action', reqData);
    set({ gameState: res.data });
  },

  buyItem: async (itemIndex) => {
    const res = await api.post('/shop/buy', { item_index: itemIndex });
    set({ gameState: res.data });
  },

  leaveShop: async () => {
    const res = await api.post('/leave_shop');
    set({ gameState: res.data });
  }
}));
