import React from "react";

export default function SidebarWidget() {
  return (
    <div
      className={`
        mx-auto mb-10 w-full max-w-60 rounded-2xl bg-gray-50 px-4 py-5 text-center dark:bg-white/[0.03]`}
    >
      <a
        href="/modules"
        className="flex items-center justify-center p-3 font-medium text-white rounded-lg bg-red-500 text-theme-sm hover:bg-red-600 transition-colors"
      >
        SALIR
      </a>
    </div>
  );
}
