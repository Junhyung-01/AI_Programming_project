import React, { useEffect } from 'react';
import { useStore } from './store';
import StartScreen from './components/StartScreen';
import LobbyScreen from './components/LobbyScreen';
import BattleScreen from './components/BattleScreen';
import ShopScreen from './components/ShopScreen';

function App() {
  const { gameState, fetchGameData } = useStore();

  useEffect(() => {
    fetchGameData();
  }, [fetchGameData]);

  return (
    <div className="app-container">
      {!gameState ? (
        <StartScreen />
      ) : gameState.game_over ? (
        <div style={{ textAlign: 'center', marginTop: 100 }}>
          <h1 style={{ color: 'red', fontSize: '3rem' }}>GAME OVER</h1>
          <button className="btn" onClick={() => window.location.reload()} style={{ marginTop: 20 }}>
            처음부터 다시 시작
          </button>
        </div>
      ) : gameState.game_clear ? (
        <div style={{ textAlign: 'center', marginTop: 100 }}>
          <h1 style={{ color: 'gold', fontSize: '3rem' }}>🏆 게임 클리어!</h1>
          <p style={{ fontSize: '1.2rem', margin: '20px 0' }}>모든 챕터를 정복했습니다. 축하합니다!</p>
          <button className="btn" onClick={() => window.location.reload()}>
            새로운 모험 시작
          </button>
        </div>
      ) : gameState.in_battle ? (
        <BattleScreen />
      ) : gameState.in_shop ? (
        <ShopScreen />
      ) : (
        <LobbyScreen />
      )}
    </div>
  );
}

export default App;
