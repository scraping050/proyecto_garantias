import ChatbotWidget from '../components/ChatbotWidget';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24 bg-gray-50 dark:bg-zinc-950">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex">
        <div className="fixed left-0 top-0 flex w-full justify-center border-b border-gray-300 bg-gradient-to-b from-zinc-200 pb-6 pt-8 backdrop-blur-2xl dark:border-neutral-800 dark:bg-zinc-800/30 dark:from-inherit lg:static lg:w-auto  lg:rounded-xl lg:border lg:bg-gray-200 lg:p-4 lg:dark:bg-zinc-800/30">
          <p className="flex justify-center text-center text-2xl font-bold">
            Garantias SEACE &nbsp;
            <code className="font-mono font-bold">Chatbot Harness</code>
          </p>
        </div>
      </div>

      <div className="relative flex place-items-center before:absolute before:h-[300px] before:w-[480px] before:-translate-x-1/2 before:rounded-full before:bg-gradient-to-br before:from-transparent before:to-blue-700 before:opacity-10 after:absolute after:-z-20 after:h-[180px] after:w-[240px] after:translate-x-1/3 after:bg-gradient-to-t after:from-sky-900 after:via-sky-900 after:blur-2xl after:content-[''] before:dark:bg-gradient-to-br before:dark:from-transparent before:dark:to-blue-700 before:dark:opacity-10 after:dark:from-sky-900 after:dark:via-[#0141ff] after:dark:opacity-40 before:lg:h-[360px] z-[-1]">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600 mb-4">
            Modulo AURA
          </h1>
          <p className="text-gray-500 max-w-lg mx-auto">
            Este es un entorno de pruebas (Harness) para el módulo de chat.
            Interactúa con el widget en la esquina inferior derecha.
          </p>
          <ul className="mt-8 text-left text-gray-500 bg-white dark:bg-zinc-900 p-6 rounded-xl shadow-sm border border-gray-200 dark:border-zinc-800">
            <li className="mb-2">✅ Conexión a BD: <strong>garantias_seace</strong></li>
            <li className="mb-2">✅ Modelo LLM: <strong>Llama3 (Groq)</strong></li>
            <li className="mb-2">✅ Voz: <strong>Web Speech API</strong></li>
          </ul>
        </div>
      </div>

      {/* The Chatbot Widget */}
      <ChatbotWidget />
    </main>
  );
}
