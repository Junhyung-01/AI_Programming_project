import React from 'react';
import { useStore } from '../store';
import { ShoppingCart, LogOut } from 'lucide-react';

export default function ShopScreen() {
  const { gameState, gameData, buyItem, leaveShop } = useStore();
  const p = gameState?.player;

  if (!p) return null;

  return (
    <div style={{ maxWidth: 800, margin: '40px auto', padding: 20 }}>
      <div className="glass-panel" style={{ width: '100%', display: 'flex', flexDirection: 'column' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ display: 'flex', alignItems: 'center', gap: 10, color: 'var(--accent-color)' }}><ShoppingCart /> 상점</h2>
          <div style={{ display: 'flex', alignItems: 'center', gap: 20 }}>
            <span style={{ color: '#fbbf24', fontWeight: 'bold', fontSize: '1.2rem' }}>💰 보유: {p.gold} G</span>
            <button className="btn btn-secondary" onClick={leaveShop} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <LogOut size={18} /> 상점 나가기
            </button>
          </div>
        </div>
        
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: 12 }}>
          {gameData?.items.map((item: any, idx: number) => {
            const canUse = !item.allowed || item.allowed.includes(p.job_class);
            const canAfford = p.gold >= item.price;
            return (
              <div key={idx} style={{ 
                display: 'flex', justifyContent: 'space-between', alignItems: 'center', 
                background: 'rgba(255,255,255,0.05)', padding: 20, borderRadius: 12,
                border: '1px solid var(--panel-border)',
                opacity: canUse ? 1 : 0.6
              }}>
                <div>
                  <h4 style={{ margin: 0, display: 'flex', alignItems: 'center', gap: 8, fontSize: '1.2rem' }}>
                    {item.name} 
                    {!canUse && <span style={{ fontSize: '0.9rem', color: 'red' }}>(착용 불가)</span>}
                  </h4>
                  <div style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: 8 }}>
                    {item.type === 'potion' ? `${item.power} 회복` : `ATK+${item.atk || 0} HP+${item.hp || 0} DEF+${item.def || 0}`}
                  </div>
                </div>
                <button 
                  className="btn" 
                  disabled={!canUse || !canAfford}
                  onClick={() => buyItem(idx)}
                  style={{ 
                    padding: '12px 24px', 
                    fontSize: '1.1rem',
                    background: canAfford && canUse ? 'var(--accent-color)' : '#374151',
                    cursor: canAfford && canUse ? 'pointer' : 'not-allowed'
                  }}
                >
                  {item.price} G
                </button>
              </div>
            );
          })}
        </div>

        {gameState.logs.length > 0 && (
          <div style={{ marginTop: 20 }}>
            <div className="log-container" style={{ height: 100 }}>
              {[...gameState.logs].reverse().slice(0, 3).map((log, i) => (
                <div key={i} className="log-entry" style={{ opacity: 1 - (i * 0.2) }}>{log}</div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
