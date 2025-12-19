import React from 'react';

const StatCard = ({ title, value, subValue, icon: Icon, trend, color }) => {
  return (
    <div className="bg-[#151E32] p-6 rounded-2xl border border-[#1E293B] hover:border-[#334155] transition-all duration-300">
      <div className="flex justify-between items-start">
        <div>
          <p className="text-slate-400 text-sm font-medium mb-1">{title}</p>
          <h3 className="text-2xl font-bold text-white">{value}</h3>
        </div>
        <div className={`p-3 rounded-xl bg-opacity-10 ${color}`}>
          <Icon size={20} className={color.replace('bg-', 'text-')} />
        </div>
      </div>
      {subValue && (
        <div className="mt-4 flex items-center gap-2">
          <span className={`text-xs font-medium px-2 py-0.5 rounded ${trend === 'up' ? 'text-emerald-400 bg-emerald-400/10' : trend === 'down' ? 'text-rose-400 bg-rose-400/10' : 'text-slate-400 bg-slate-400/10'}`}>
            {subValue}
          </span>
          <span className="text-slate-500 text-xs">vs last hour</span>
        </div>
      )}
    </div>
  );
};

export default StatCard;