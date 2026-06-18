type Token = {
  surface: string;
  pos: string;
  stem: string;
  tense: string | null;
  aspect: string | null;
};

const POS_COLOR: Record<string, string> = {
  V:     "text-violet-400 bg-violet-500/10",
  N:     "text-sky-400    bg-sky-500/10",
  Adj:   "text-amber-400  bg-amber-500/10",
  Pron:  "text-teal-400   bg-teal-500/10",
  PossN: "text-teal-300   bg-teal-500/10",
  Det:   "text-slate-300  bg-slate-700/50",
  P:     "text-orange-400 bg-orange-500/10",
  T:     "text-cyan-400   bg-cyan-500/10",
  QN:    "text-pink-400   bg-pink-500/10",
  Neg:   "text-red-400    bg-red-500/10",
  CAUS_V:"text-fuchsia-400 bg-fuchsia-500/10",
};

function PosTag({ pos }: { pos: string }) {
  const cls = POS_COLOR[pos] ?? "text-slate-400 bg-slate-700/50";
  return (
    <span className={`px-1.5 py-0.5 rounded text-xs font-mono font-semibold ${cls}`}>
      {pos}
    </span>
  );
}

export default function TokenTable({ tokens }: { tokens: Token[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b border-slate-800 text-slate-500 text-xs uppercase tracking-wider">
            <th className="text-left pb-2 pr-6">Word</th>
            <th className="text-left pb-2 pr-6">Tag</th>
            <th className="text-left pb-2 pr-6">Stem</th>
            <th className="text-left pb-2">Tense · Aspect</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-800/60">
          {tokens.map((tok, i) => (
            <tr key={i} className="py-1">
              <td className="py-2 pr-6">
                <span className="sigan text-slate-100 font-medium">{tok.surface}</span>
              </td>
              <td className="py-2 pr-6">
                <PosTag pos={tok.pos} />
              </td>
              <td className="py-2 pr-6 sigan text-slate-400 text-xs">
                {tok.stem !== tok.surface ? tok.stem : "—"}
              </td>
              <td className="py-2 text-slate-400 text-xs">
                {tok.tense
                  ? <span>{tok.tense} · {tok.aspect}</span>
                  : "—"}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
