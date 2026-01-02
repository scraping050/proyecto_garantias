
module.exports = {
    apps: [
        {
            name: "nextjs-mcqs",
            cwd: "./seace/proyecto_garantias/free-nextjs-admin-dashboard-main",
            script: "npm",
            args: "start",
            env: {
                NEXT_PUBLIC_API_URL: "https://api.mcqs-jcq.com",
                PORT: 3000
            }
        },
        {
            name: "fastapi-mcqs",
            cwd: ".",
            script: "python3",
            args: "-m uvicorn app.main:app --host 0.0.0.0 --port 8000",
            env: {
                PYTHONPATH: "/home/mcqs-jcq/htdocs/mcqs-jcq.com",
                CORS_ORIGINS: '["https://mcqs-jcq.com", "https://api.mcqs-jcq.com"]'
            }
        }
    ]
}