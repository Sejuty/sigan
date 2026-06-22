export type TreeNode = {
  symbol: string;
  token?: string;
  tense?: string | null;
  aspect?: string | null;
  children: TreeNode[];
};

const SYM_COLOR: Record<string, string> = {
  S:        "text-violet-400",
  NP:       "text-sky-400",
  VP:       "text-emerald-400",
  PP:       "text-orange-400",
  S_Q:      "text-pink-400",
  S_CAUS:   "text-fuchsia-400",
  VP_PP:    "text-emerald-300",
  VP_T:     "text-emerald-300",
  VP_PP_T:  "text-emerald-300",
  VP_LOC:   "text-emerald-300",
  NP_A:     "text-sky-300",
  NEG_V:    "text-red-400",
  CAUS_BODY:"text-fuchsia-300",
  NP_V:     "text-sky-300",
  VP_Q:     "text-pink-300",
  Loc:      "text-orange-300",
  Greet:    "text-yellow-400",
  PropN:    "text-sky-300",
};

function NodeLine({
  node,
  prefix,
  isLast,
}: {
  node: TreeNode;
  prefix: string;
  isLast: boolean;
}) {
  const connector = isLast ? "└── " : "├── ";
  const childPrefix = prefix + (isLast ? "    " : "│   ");
  const symColor = SYM_COLOR[node.symbol] ?? "text-slate-300";
  const isLeaf = node.children.length === 0;

  return (
    <div>
      <div className="flex items-baseline gap-1 font-mono text-sm leading-6">
        <span className="text-slate-600 select-none whitespace-pre">{prefix + connector}</span>
        <span className={`font-semibold ${symColor}`}>{node.symbol}</span>
        {isLeaf && node.token && (
          <>
            <span className="text-slate-600 mx-0.5">›</span>
            <span className="sigan text-slate-200">&quot;{node.token}&quot;</span>
            {node.tense && (
              <span className="text-xs text-slate-500 ml-1">
                [{node.tense}·{node.aspect}]
              </span>
            )}
          </>
        )}
      </div>
      {node.children.map((child, i) => (
        <NodeLine
          key={i}
          node={child}
          prefix={childPrefix}
          isLast={i === node.children.length - 1}
        />
      ))}
    </div>
  );
}

export default function ParseTree({ tree }: { tree: TreeNode }) {
  const symColor = SYM_COLOR[tree.symbol] ?? "text-slate-300";
  return (
    <div className="font-mono text-sm leading-6 scrollbar-thin overflow-x-auto">
      <div className={`font-semibold ${symColor} mb-0.5`}>{tree.symbol}</div>
      {tree.children.map((child, i) => (
        <NodeLine
          key={i}
          node={child}
          prefix=""
          isLast={i === tree.children.length - 1}
        />
      ))}
    </div>
  );
}
