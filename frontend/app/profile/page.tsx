'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { HeaderActions } from '@/components/layout/header-actions';
import { User, Shield, Key, Smartphone, Upload, Check, AlertCircle, Save, Activity, Users, Edit2, X, Trash2, UserPlus } from 'lucide-react';
import { api } from '@/lib/api';
import { PinVerificationModal } from '@/components/admin/pin-verification-modal';
import { AddUserModal } from '@/components/admin/add-user-modal';
import { DeleteUserModal } from '@/components/admin/delete-user-modal';
import { ConfirmationModal } from '@/components/ui/confirmation-modal';


export default function ProfilePage() {
    const router = useRouter();
    const [activeTab, setActiveTab] = useState('personal');
    const [loading, setLoading] = useState(false);
    const [successMessage, setSuccessMessage] = useState('');
    const [user, setUser] = useState<any>(null);
    const [sessions, setSessions] = useState<any[]>([]);

    // Form States
    const [formData, setFormData] = useState({
        nombre: '',
        apellidos: '',
        email: '',
        phone_number: '',
        job_title: ''
    });
    useEffect(() => {
        fetchUserData();
        fetchSessions();
    }, []);

    const fetchUserData = async () => {
        try {
            const response = await api.get('/api/users/me');
            const updatedUser = response.data;
            setUser(updatedUser);

            // Update localStorage to keep header in sync
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                const parsed = JSON.parse(storedUser);
                const newUserData = { ...parsed, ...updatedUser };
                localStorage.setItem('user', JSON.stringify(newUserData));

                // Dispatch event for header update
                window.dispatchEvent(new Event('userUpdated'));
            }

            setFormData({
                nombre: updatedUser.nombre || '',
                apellidos: updatedUser.apellidos || '',
                email: updatedUser.email || '',
                phone_number: updatedUser.phone_number || '',
                job_title: updatedUser.job_title || ''
            });
        } catch (error) {
            console.error('Error fetching user:', error);
        }
    };

    const fetchSessions = async () => {
        try {
            const response = await api.get('/api/users/me/sessions');
            setSessions(response.data);
        } catch (error) {
            console.error('Error fetching sessions:', error);
        }
    };

    const handleUpdateProfile = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            await api.put('/api/users/me', formData);
            setSuccessMessage('Perfil actualizado correctamente');
            fetchUserData();
            setTimeout(() => setSuccessMessage(''), 3000);
        } catch (error) {
            console.error('Error updating profile:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>, type: 'avatar' | 'signature') => {
        const file = e.target.files?.[0];
        if (!file) return;

        const formData = new FormData();
        formData.append('file', file);

        try {
            await api.post(`/api/users/me/${type}`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            fetchUserData();
            setSuccessMessage(`${type === 'avatar' ? 'Foto' : 'Firma'} actualizada`);
            setTimeout(() => setSuccessMessage(''), 3000);
        } catch (error) {
            console.error(`Error uploading ${type}:`, error);
        }
    };

    const [isDeleteAvatarModalOpen, setIsDeleteAvatarModalOpen] = useState(false);

    const handleDeleteAvatarClick = () => {
        setIsDeleteAvatarModalOpen(true);
    };

    const confirmDeleteAvatar = async () => {
        try {
            await api.delete('/api/users/me/avatar');
            fetchUserData();
            setSuccessMessage('Foto de perfil eliminada');
            setTimeout(() => setSuccessMessage(''), 3000);
            setIsDeleteAvatarModalOpen(false);
        } catch (error) {
            console.error('Error deleting avatar:', error);
        }
    };

    const handleRevokeSession = async (sessionId: number) => {
        try {
            await api.delete(`/api/users/me/sessions/${sessionId}`);
            fetchSessions();
        } catch (error) {
            console.error('Error revoking session:', error);
        }
    };

    return (
        <div className="min-h-screen bg-slate-50 dark:bg-slate-900 transition-colors duration-500 bg-[url('/grid.svg')] bg-fixed">
            {/* Header */}
            <div className="h-20 bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl border-b border-slate-200 dark:border-slate-700 flex items-center justify-between px-8 sticky top-0 z-40 shadow-sm">
                <div className="flex items-center gap-4">
                    <button onClick={() => router.back()} className="p-2.5 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-full transition-colors group">
                        <i className="fas fa-arrow-left text-slate-600 dark:text-slate-300 group-hover:-translate-x-1 transition-transform"></i>
                    </button>
                    <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-slate-800 to-slate-600 dark:from-white dark:to-slate-300">Mi Perfil</h1>
                </div>
                <HeaderActions />
            </div>

            <div className="max-w-7xl mx-auto p-8">
                <div className="grid grid-cols-12 gap-8">
                    {/* Sidebar Navigation */}
                    <div className="col-span-12 md:col-span-3 space-y-3 sticky top-24 self-start">
                        <div className="bg-white/50 dark:bg-slate-800/50 backdrop-blur-xl rounded-3xl p-4 border border-white/20 shadow-xl shadow-slate-200/50 dark:shadow-none">
                            <NavButton
                                active={activeTab === 'personal'}
                                onClick={() => setActiveTab('personal')}
                                icon={<User size={20} />}
                                label="Información Personal"
                                description="Datos básicos y contacto"
                            />
                            {user?.perfil?.toUpperCase() === 'DIRECTOR' && (
                                <NavButton
                                    active={activeTab === 'security'}
                                    onClick={() => setActiveTab('security')}
                                    icon={<Shield size={20} />}
                                    label="Seguridad"
                                    description="Contraseña y PIN"
                                />
                            )}
                            {user?.perfil?.toUpperCase() === 'DIRECTOR' && (
                                <NavButton
                                    active={activeTab === 'users'}
                                    onClick={() => setActiveTab('users')}
                                    icon={<Users size={20} />}
                                    label="Usuarios"
                                    description="Gestión de usuarios"
                                />
                            )}
                            <NavButton
                                active={activeTab === 'sessions'}
                                onClick={() => setActiveTab('sessions')}
                                icon={<Smartphone size={20} />}
                                label="Dispositivos"
                                description="Sesiones activas"
                            />
                            <NavButton
                                active={activeTab === 'activity'}
                                onClick={() => setActiveTab('activity')}
                                icon={<Activity size={20} />}
                                label="Historial"
                                description="Actividad reciente"
                            />
                        </div>
                    </div>

                    {/* Content Area */}
                    <div className="col-span-12 md:col-span-9">
                        {successMessage && (
                            <div className="mb-6 p-4 bg-green-50/80 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-2xl flex items-center gap-3 text-green-700 dark:text-green-300 animate-in slide-in-from-top-2 backdrop-blur-sm shadow-lg shadow-green-500/10">
                                <div className="w-8 h-8 rounded-full bg-green-100 dark:bg-green-900/50 flex items-center justify-center shrink-0">
                                    <Check size={16} />
                                </div>
                                <span className="font-medium">{successMessage}</span>
                            </div>
                        )}

                        {activeTab === 'personal' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
                                {/* Identity Card */}
                                <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-500/10 to-cyan-500/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 pointer-events-none"></div>

                                    <div className="flex items-start justify-between mb-10 relative z-10">
                                        <div>
                                            <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">Identidad Digital</h2>
                                            <p className="text-slate-500 dark:text-slate-400">Gestiona tu imagen y firma digital</p>
                                        </div>
                                        <span className="px-4 py-1.5 bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-300 rounded-full text-xs font-bold uppercase tracking-wider border border-blue-100 dark:border-blue-800">
                                            {user?.perfil || 'Usuario'}
                                        </span>
                                    </div>

                                    <div className="flex flex-col md:flex-row gap-12 items-center relative z-10">
                                        {/* Avatar Upload */}
                                        <div className="relative group/avatar">
                                            <div className="w-40 h-40 rounded-full p-1 bg-gradient-to-tr from-blue-600 via-cyan-500 to-blue-400 shadow-2xl shadow-blue-500/30">
                                                <div className="w-full h-full rounded-full bg-white dark:bg-slate-800 flex items-center justify-center overflow-hidden relative">
                                                    {user?.avatar_url ? (
                                                        <img src={user.avatar_url} alt="Avatar" className="w-full h-full object-cover transition-transform duration-500 group-hover/avatar:scale-110" />
                                                    ) : (
                                                        <span className="text-5xl font-bold text-slate-300 dark:text-slate-600 select-none">
                                                            {user?.nombre?.charAt(0).toUpperCase() || 'U'}
                                                        </span>
                                                    )}
                                                </div>
                                            </div>

                                            <label className="absolute bottom-2 right-2 p-3 bg-white dark:bg-slate-700 rounded-full shadow-lg cursor-pointer hover:scale-110 transition-all border border-slate-100 dark:border-slate-600 z-20 hover:shadow-xl text-blue-600 dark:text-blue-400">
                                                <Upload size={18} />
                                                <input type="file" className="hidden" accept="image/*" onChange={(e) => handleFileUpload(e, 'avatar')} />
                                            </label>

                                            {user?.avatar_url && (
                                                <button
                                                    onClick={handleDeleteAvatarClick}
                                                    className="absolute top-2 right-2 p-3 bg-red-50 dark:bg-red-900/80 rounded-full shadow-lg cursor-pointer hover:scale-110 transition-all border border-red-100 dark:border-red-800 z-20 text-red-500 dark:text-red-300 hover:bg-red-100 dark:hover:bg-red-900"
                                                    title="Eliminar foto"
                                                >
                                                    <Trash2 size={18} />
                                                </button>
                                            )}
                                        </div>

                                        {/* Signature Upload */}
                                        <div className="flex-1 w-full">
                                            <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-3">Firma Digital / Sello</label>
                                            <div className="border-2 border-dashed border-slate-300 dark:border-slate-600 rounded-2xl p-8 flex flex-col items-center justify-center text-center hover:bg-slate-50/50 dark:hover:bg-slate-800/50 hover:border-blue-400 dark:hover:border-blue-500 transition-all duration-300 relative group cursor-pointer bg-slate-50/30 dark:bg-slate-900/20">
                                                {user?.digital_signature_url ? (
                                                    <img src={user.digital_signature_url} alt="Firma" className="h-24 object-contain drop-shadow-md transition-transform group-hover:scale-105" />
                                                ) : (
                                                    <div className="text-slate-400 group-hover:text-blue-500 transition-colors">
                                                        <div className="w-16 h-16 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-50 dark:group-hover:bg-blue-900/20 transition-colors">
                                                            <Upload size={28} className="opacity-50 group-hover:opacity-100" />
                                                        </div>
                                                        <p className="font-medium">Click para subir imagen de firma</p>
                                                        <p className="text-xs opacity-70 mt-1">PNG transparente recomendado</p>
                                                    </div>
                                                )}
                                                <input type="file" className="absolute inset-0 opacity-0 cursor-pointer" accept="image/*" onChange={(e) => handleFileUpload(e, 'signature')} />
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                {/* Confirmation Modal */}
                                <ConfirmationModal
                                    isOpen={isDeleteAvatarModalOpen}
                                    onClose={() => setIsDeleteAvatarModalOpen(false)}
                                    onConfirm={confirmDeleteAvatar}
                                    title="Confirmar Eliminación"
                                    description="¿Estás seguro de que deseas eliminar tu foto de perfil?"
                                    confirmText="Sí, Eliminar"
                                    cancelText="Cancelar"
                                    variant="danger"
                                />

                                {/* Personal Info Form */}
                                <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700">
                                    <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-8">Información Básica</h2>
                                    <form onSubmit={handleUpdateProfile} className="grid grid-cols-1 md:grid-cols-2 gap-8">
                                        <InputGroup label="Nombre" value={formData.nombre} onChange={(v: string) => setFormData({ ...formData, nombre: v })} />
                                        <InputGroup label="Apellidos" value={formData.apellidos} onChange={(v: string) => setFormData({ ...formData, apellidos: v })} />

                                        <div className="relative">
                                            <InputGroup label="Correo Electrónico" value={formData.email} onChange={(v: string) => setFormData({ ...formData, email: v })} type="email" />
                                            {user?.email_verified && (
                                                <div className="absolute top-10 right-4 text-green-500 bg-green-50 dark:bg-green-900/30 p-1 rounded-full" title="Correo Verificado">
                                                    <Check size={14} />
                                                </div>
                                            )}
                                        </div>

                                        <InputGroup label="Celular" value={formData.phone_number} onChange={(v: string) => setFormData({ ...formData, phone_number: v })} placeholder="+51 999 999 999" />
                                        <InputGroup label="Cargo / Puesto" value={formData.job_title} onChange={(v: string) => setFormData({ ...formData, job_title: v })} className="md:col-span-2" />

                                        <div className="md:col-span-2 flex justify-end mt-6">
                                            <button
                                                type="submit"
                                                disabled={loading}
                                                className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-xl font-bold flex items-center gap-3 transition-all hover:shadow-xl hover:shadow-blue-500/30 hover:-translate-y-0.5 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
                                            >
                                                {loading ? <span className="animate-spin">⏳</span> : <Save size={20} />}
                                                Guardar Cambios
                                            </button>
                                        </div>
                                    </form>
                                </div>
                            </div>
                        )}

                        {activeTab === 'security' && (
                            <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
                                {/* Password Change Form */}
                                <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700">
                                    <div className="flex items-center gap-5 mb-8">
                                        <div className="w-14 h-14 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center text-blue-600 dark:text-blue-400 shadow-inner">
                                            <Key size={28} />
                                        </div>
                                        <div>
                                            <h2 className="text-2xl font-bold text-slate-800 dark:text-white">Contraseña</h2>
                                            <p className="text-slate-500 dark:text-slate-400 mt-1">Actualiza tu contraseña de acceso al sistema</p>
                                        </div>
                                    </div>

                                    <SecurityForm
                                        type="password"
                                        endpoint="/api/users/me/password"
                                        onSuccess={() => {
                                            setSuccessMessage('Contraseña actualizada correctamente');
                                            setTimeout(() => setSuccessMessage(''), 3000);
                                        }}
                                    />
                                </div>

                                {user?.perfil?.toUpperCase() === 'DIRECTOR' && (
                                    <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700">
                                        <div className="flex items-center gap-5 mb-8">
                                            <div className="w-14 h-14 bg-purple-100 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center text-purple-600 dark:text-purple-400 shadow-inner">
                                                <Shield size={28} />
                                            </div>
                                            <div>
                                                <h2 className="text-2xl font-bold text-slate-800 dark:text-white">PIN de Seguridad</h2>
                                                <p className="text-slate-500 dark:text-slate-400 mt-1">Código de 6 dígitos para autorizar operaciones sensibles</p>
                                            </div>
                                        </div>

                                        <SecurityForm
                                            type="pin"
                                            endpoint="/api/users/me/pin"
                                            onSuccess={() => {
                                                setSuccessMessage('PIN de seguridad actualizado correctamente');
                                                setTimeout(() => setSuccessMessage(''), 3000);
                                            }}
                                        />
                                    </div>
                                )}
                            </div>
                        )}

                        {activeTab === 'sessions' && (
                            <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700 animate-in fade-in slide-in-from-right-4 duration-500">
                                <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">Sesiones Activas</h2>
                                <p className="text-slate-500 dark:text-slate-400 mb-8">Gestiona los dispositivos donde has iniciado sesión.</p>

                                <div className="space-y-4">
                                    {sessions.map((session) => (
                                        <div key={session.id} className="flex items-center justify-between p-5 rounded-2xl bg-slate-50 dark:bg-slate-900/50 border border-slate-100 dark:border-slate-700/50 hover:bg-white dark:hover:bg-slate-800 transition-all duration-300 shadow-sm hover:shadow-md group">
                                            <div className="flex items-center gap-5">
                                                <div className="w-12 h-12 rounded-2xl bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform">
                                                    <Smartphone size={24} />
                                                </div>
                                                <div>
                                                    <p className="font-bold text-slate-800 dark:text-white text-base">{session.user_agent || 'Dispositivo Desconocido'}</p>
                                                    <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">
                                                        {session.ip_address} • Última actividad: {new Date(session.last_active).toLocaleString()}
                                                    </p>
                                                </div>
                                            </div>
                                            {session.is_active && (
                                                <button
                                                    onClick={() => handleRevokeSession(session.id)}
                                                    className="text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 px-4 py-2 rounded-xl text-sm font-bold transition-colors"
                                                >
                                                    Cerrar Sesión
                                                </button>
                                            )}
                                        </div>
                                    ))}

                                    {sessions.length === 0 && (
                                        <div className="text-center py-16 text-slate-400">
                                            <Smartphone size={48} className="mx-auto mb-4 opacity-20" />
                                            <p>No hay otras sesiones activas.</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        )}

                        {activeTab === 'activity' && (
                            <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700 animate-in fade-in slide-in-from-right-4 duration-500">
                                <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">Historial de Actividad</h2>
                                <p className="text-slate-500 dark:text-slate-400 mb-8">Registro de tus últimas acciones en la plataforma.</p>
                                <ActivityList />
                            </div>
                        )}

                        {activeTab === 'users' && user?.perfil?.toUpperCase() === 'DIRECTOR' && (
                            <div className="bg-white/80 dark:bg-slate-800/80 backdrop-blur-xl rounded-3xl p-8 shadow-xl shadow-slate-200/50 dark:shadow-none border border-white/50 dark:border-slate-700 animate-in fade-in slide-in-from-right-4 duration-500">
                                <div className="flex items-center justify-between mb-8">
                                    <div>
                                        <h2 className="text-2xl font-bold text-slate-800 dark:text-white mb-2">Gestión de Usuarios</h2>
                                        <p className="text-slate-500 dark:text-slate-400">Administra los accesos y contraseñas de los colaboradores.</p>
                                    </div>
                                </div>
                                <UsersManagement />
                            </div>
                        )}


                    </div>
                </div>
            </div>
        </div >
    );
}

function SecurityForm({ type, endpoint, onSuccess }: { type: 'password' | 'pin', endpoint: string, onSuccess: () => void }) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [data, setData] = useState({
        current: '',
        new: '',
        confirm: ''
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        if (data.new !== data.confirm) {
            setError(`Las nuevas ${type === 'password' ? 'contraseñas' : 'PINs'} no coinciden`);
            setLoading(false);
            return;
        }

        try {
            const payload = type === 'password'
                ? { current_password: data.current, new_password: data.new, confirm_password: data.confirm }
                : { current_pin: data.current, new_pin: data.new, confirm_pin: data.confirm };

            await api.put(endpoint, payload);
            onSuccess();
            setData({ current: '', new: '', confirm: '' });
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Error al actualizar');
        } finally {
            setLoading(false);
        }
    };

    const labels = type === 'password'
        ? { current: 'Contraseña Actual', new: 'Nueva Contraseña', confirm: 'Confirmar Contraseña' }
        : { current: 'PIN Actual', new: 'Nuevo PIN (6 dígitos)', confirm: 'Confirmar PIN' };

    return (
        <form onSubmit={handleSubmit} className="space-y-5 max-w-lg">
            {error && (
                <div className="p-4 bg-red-50/50 dark:bg-red-900/10 border border-red-100 dark:border-red-800/30 text-red-600 dark:text-red-400 rounded-xl text-sm flex items-center gap-3 animate-in slide-in-from-top-2">
                    <AlertCircle size={18} />
                    {error}
                </div>
            )}

            <InputGroup
                label={labels.current}
                type="password"
                value={data.current}
                onChange={(v: string) => setData({ ...data, current: v })}
                placeholder="••••••••"
            />

            <div className="grid grid-cols-2 gap-5">
                <InputGroup
                    label={labels.new}
                    type="password"
                    value={data.new}
                    onChange={(v: string) => setData({ ...data, new: v })}
                    placeholder="••••••••"
                />
                <InputGroup
                    label={labels.confirm}
                    type="password"
                    value={data.confirm}
                    onChange={(v: string) => setData({ ...data, confirm: v })}
                    placeholder="••••••••"
                />
            </div>

            <div className="flex justify-end pt-4">
                <button
                    type="submit"
                    disabled={loading || !data.current || !data.new || !data.confirm}
                    className="bg-slate-900 dark:bg-white text-white dark:text-slate-900 hover:bg-slate-800 dark:hover:bg-slate-100 px-8 py-3 rounded-xl font-bold flex items-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-slate-900/20 hover:shadow-xl hover:-translate-y-0.5"
                >
                    {loading ? <span className="animate-spin">⏳</span> : <Save size={18} />}
                    Actualizar {type === 'password' ? 'Contraseña' : 'PIN'}
                </button>
            </div>
        </form>
    );
}

function NavButton({ active, onClick, icon, label, description }: any) {
    return (
        <button
            onClick={onClick}
            className={`w-full text-left p-4 rounded-2xl transition-all duration-300 flex items-center gap-4 group relative overflow-hidden ${active
                ? 'bg-gradient-to-r from-blue-600 to-blue-500 text-white shadow-lg shadow-blue-500/30 ring-2 ring-blue-500/20'
                : 'bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700/50 hover:text-slate-900 dark:hover:text-slate-200'
                }`}
        >
            <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-all duration-300 ${active
                ? 'bg-white/20 text-white shadow-inner'
                : 'bg-slate-100 dark:bg-slate-700/50 text-slate-500 dark:text-slate-400 group-hover:scale-110 group-hover:bg-blue-50 dark:group-hover:bg-blue-900/20 group-hover:text-blue-600 dark:group-hover:text-blue-400'
                }`}>
                {icon}
            </div>
            <div className="relative z-10">
                <p className={`font-bold text-sm mb-0.5 ${active ? 'text-white' : 'text-slate-700 dark:text-slate-200'}`}>{label}</p>
                <p className={`text-xs ${active ? 'text-blue-100' : 'text-slate-500 dark:text-slate-400'}`}>{description}</p>
            </div>
            {active && (
                <div className="absolute right-0 top-0 bottom-0 w-1 bg-white/20 backdrop-blur-sm"></div>
            )}
        </button>
    );
}

function InputGroup({ label, value, onChange, type = "text", placeholder, className }: any) {
    const [isFocused, setIsFocused] = useState(false);

    return (
        <div className={className}>
            <label className={`block text-sm font-bold mb-2 transition-colors ${isFocused ? 'text-blue-600 dark:text-blue-400' : 'text-slate-700 dark:text-slate-300'}`}>
                {label}
            </label>
            <div className="relative">
                <input
                    type={type}
                    value={value}
                    onChange={(e) => onChange(e.target.value)}
                    onFocus={() => setIsFocused(true)}
                    onBlur={() => setIsFocused(false)}
                    placeholder={placeholder}
                    className={`w-full px-5 py-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/50 border-2 transition-all duration-300 outline-none text-slate-800 dark:text-white placeholder-slate-400 ${isFocused
                        ? 'border-blue-500 ring-4 ring-blue-500/10 bg-white dark:bg-slate-900'
                        : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                        }`}
                />
            </div>
        </div>
    );
}

function ActivityList() {
    const [logs, setLogs] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await api.get('/api/users/me/audit-logs');
                setLogs(response.data);
            } catch (error) {
                console.error('Error fetching logs:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchLogs();
    }, []);

    if (loading) return <div className="text-center py-12 text-slate-500 animate-pulse">Cargando actividad...</div>;

    if (logs.length === 0) {
        return (
            <div className="text-center py-16 text-slate-400 bg-slate-50/50 dark:bg-slate-900/20 rounded-2xl border border-dashed border-slate-200 dark:border-slate-700">
                <Activity size={48} className="mx-auto mb-4 opacity-20" />
                <p>No hay actividad registrada recientemente.</p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {logs.map((log) => (
                <div key={log.id} className="flex items-start gap-5 p-5 rounded-2xl bg-white dark:bg-slate-800 border border-slate-100 dark:border-slate-700/50 shadow-sm hover:shadow-md transition-all duration-300 group">
                    <div className="w-10 h-10 rounded-full bg-blue-50 dark:bg-blue-900/20 flex items-center justify-center text-blue-600 dark:text-blue-400 shrink-0 mt-1 group-hover:scale-110 transition-transform">
                        <Activity size={18} />
                    </div>
                    <div>
                        <p className="font-bold text-slate-800 dark:text-white text-base">{log.action}</p>
                        <p className="text-sm text-slate-600 dark:text-slate-300 mt-1 leading-relaxed">{log.details}</p>
                        <div className="flex items-center gap-4 mt-3 text-xs font-medium text-slate-400">
                            <span className="flex items-center gap-1.5">
                                <i className="far fa-clock"></i>
                                {new Date(log.created_at).toLocaleString()}
                            </span>
                            {log.ip_address && (
                                <span className="flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-slate-100 dark:bg-slate-700/50">
                                    <i className="fas fa-globe"></i>
                                    {log.ip_address}
                                </span>
                            )}
                        </div>
                    </div>
                </div>
            ))}
        </div>
    );
}


function UsersManagement() {
    const [users, setUsers] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [editingUser, setEditingUser] = useState<any>(null);
    const [successMsg, setSuccessMsg] = useState('');

    // New states for add/delete functionality
    const [isAddModalOpen, setIsAddModalOpen] = useState(false);
    const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
    const [isPinModalOpen, setIsPinModalOpen] = useState(false);
    const [userToDelete, setUserToDelete] = useState<any>(null);
    const [pendingAction, setPendingAction] = useState<'add' | 'delete' | null>(null);

    useEffect(() => {
        fetchUsers();
    }, []);

    const fetchUsers = async () => {
        try {
            const response = await api.get('/api/users');
            setUsers(response.data);
        } catch (error) {
            console.error('Error fetching users:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateUser = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await api.put(`/api/users/${editingUser.id}`, editingUser);
            setSuccessMsg('Usuario actualizado correctamente');
            setEditingUser(null);
            fetchUsers();
            setTimeout(() => setSuccessMsg(''), 3000);
        } catch (error) {
            console.error('Error updating user:', error);
        }
    };

    const handleAddUserClick = () => {
        setIsAddModalOpen(true);
    };

    const handleDeleteUserClick = (user: any) => {
        setUserToDelete(user);
        setPendingAction('delete');
        setIsPinModalOpen(true);
    };

    const verifyPin = async (pin: string): Promise<boolean> => {
        try {
            const response = await api.post('/api/auth/verify-pin', { pin });
            if (response.data.valid) {
                setIsPinModalOpen(false);
                if (pendingAction === 'delete') {
                    setIsDeleteModalOpen(true);
                }
                return true;
            }
            return false;
        } catch (error) {
            console.error('Error verifying PIN:', error);
            return false;
        }
    };

    const handleUserAdded = () => {
        setSuccessMsg('Usuario creado exitosamente');
        fetchUsers();
        setTimeout(() => setSuccessMsg(''), 3000);
    };

    const handleUserDeleted = () => {
        setSuccessMsg('Usuario eliminado exitosamente');
        setUserToDelete(null);
        fetchUsers();
        setTimeout(() => setSuccessMsg(''), 3000);
    };

    if (loading) return <div className="text-center py-12 animate-pulse">Cargando usuarios...</div>;

    return (
        <div className="space-y-8">
            {successMsg && (
                <div className="p-4 bg-green-50/50 dark:bg-green-900/20 border border-green-100 dark:border-green-800/30 text-green-700 dark:text-green-300 rounded-xl flex items-center gap-3 animate-in slide-in-from-top-2">
                    <Check size={20} />
                    {successMsg}
                </div>
            )}

            {/* Add User Button */}
            <div className="flex justify-end">
                <button
                    onClick={handleAddUserClick}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold flex items-center gap-2 transition-all shadow-lg shadow-blue-500/30 hover:shadow-xl hover:-translate-y-0.5 active:scale-95"
                >
                    <UserPlus size={20} />
                    Añadir Usuario
                </button>
            </div>

            {/* Users Table */}
            <div className="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 shadow-lg shadow-slate-200/50 dark:shadow-none bg-white dark:bg-slate-800">
                <div className="overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                        <thead>
                            <tr className="bg-slate-50/80 dark:bg-slate-900/50 border-b border-slate-200 dark:border-slate-700">
                                <th className="py-4 px-6 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Usuario</th>
                                <th className="py-4 px-6 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Rol</th>
                                <th className="py-4 px-6 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Estado</th>
                                <th className="py-4 px-6 text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400 text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100 dark:divide-slate-700/50">
                            {users.map((u) => (
                                <tr key={u.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-700/30 transition-colors group">
                                    <td className="py-4 px-6">
                                        <div className="flex items-center gap-4">
                                            <div className="w-10 h-10 rounded-full bg-gradient-to-tr from-blue-100 to-indigo-100 dark:from-blue-900/30 dark:to-indigo-900/30 flex items-center justify-center text-blue-600 dark:text-blue-400 font-bold text-sm shadow-sm ring-2 ring-white dark:ring-slate-800">
                                                {u.nombre?.charAt(0) || u.id_corporativo?.charAt(0)}
                                            </div>
                                            <div>
                                                <p className="font-bold text-slate-800 dark:text-white text-sm">{u.nombre} {u.apellidos}</p>
                                                <p className="text-xs font-medium text-slate-500 dark:text-slate-400">{u.email || u.id_corporativo}</p>
                                            </div>
                                        </div>
                                    </td>
                                    <td className="py-4 px-6">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${u.perfil?.toUpperCase() === 'DIRECTOR'
                                            ? 'bg-purple-50 text-purple-600 border-purple-100 dark:bg-purple-900/20 dark:text-purple-300 dark:border-purple-800/30'
                                            : 'bg-blue-50 text-blue-600 border-blue-100 dark:bg-blue-900/20 dark:text-blue-300 dark:border-blue-800/30'
                                            }`}>
                                            {u.perfil}
                                        </span>
                                    </td>
                                    <td className="py-4 px-6">
                                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${u.activo
                                            ? 'bg-green-50 text-green-600 border-green-100 dark:bg-green-900/20 dark:text-green-300 dark:border-green-800/30'
                                            : 'bg-red-50 text-red-600 border-red-100 dark:bg-red-900/20 dark:text-red-300 dark:border-red-800/30'
                                            }`}>
                                            {u.activo ? 'Activo' : 'Inactivo'}
                                        </span>
                                    </td>
                                    <td className="py-4 px-6 text-right">
                                        <div className="flex items-center justify-end gap-3">
                                            <button
                                                onClick={() => setEditingUser({ ...u, password: '' })}
                                                className="p-2.5 bg-blue-50 hover:bg-blue-100 dark:bg-blue-900/20 dark:hover:bg-blue-900/40 rounded-xl text-blue-600 dark:text-blue-400 transition-all shadow-sm hover:shadow-md hover:-translate-y-0.5"
                                                title="Editar Usuario"
                                            >
                                                <Edit2 size={18} />
                                            </button>
                                            <button
                                                onClick={() => handleDeleteUserClick(u)}
                                                className="p-2.5 bg-red-50 hover:bg-red-100 dark:bg-red-900/20 dark:hover:bg-red-900/40 rounded-xl text-red-600 dark:text-red-400 transition-all shadow-sm hover:shadow-md hover:-translate-y-0.5"
                                                title="Eliminar Usuario"
                                            >
                                                <Trash2 size={18} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>



            {/* Edit Modal (existing) */}
            {editingUser && (
                <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4 animate-in fade-in duration-200">
                    <div className="bg-white dark:bg-slate-800 rounded-2xl p-8 w-full max-w-md shadow-2xl border border-slate-200 dark:border-slate-700 animate-in zoom-in-95 duration-200">
                        <div className="flex justify-between items-center mb-8">
                            <h3 className="text-xl font-bold text-slate-800 dark:text-white">Editar Usuario</h3>
                            <button onClick={() => setEditingUser(null)} className="p-2 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-full text-slate-500 transition-colors">
                                <X size={20} />
                            </button>
                        </div>

                        <form onSubmit={handleUpdateUser} className="space-y-5">
                            <InputGroup
                                label="ID Corporativo (Usuario)"
                                value={editingUser.id_corporativo || ''}
                                onChange={(v: string) => setEditingUser({ ...editingUser, id_corporativo: v })}
                            />
                            <InputGroup
                                label="Nombre"
                                value={editingUser.nombre || ''}
                                onChange={(v: string) => setEditingUser({ ...editingUser, nombre: v })}
                            />
                            <InputGroup
                                label="Apellidos"
                                value={editingUser.apellidos || ''}
                                onChange={(v: string) => setEditingUser({ ...editingUser, apellidos: v })}
                            />
                            <InputGroup
                                label="Nueva Contraseña (Opcional)"
                                type="password"
                                value={editingUser.password || ''}
                                onChange={(v: string) => setEditingUser({ ...editingUser, password: v })}
                                placeholder="Dejar en blanco para mantener"
                            />

                            <div className="grid grid-cols-2 gap-5">
                                <div>
                                    <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Rol</label>
                                    <div className="relative">
                                        <select
                                            value={editingUser.perfil || 'COLABORADOR'}
                                            onChange={(e) => setEditingUser({ ...editingUser, perfil: e.target.value })}
                                            className="w-full px-4 py-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-blue-500 outline-none text-slate-800 dark:text-white appearance-none cursor-pointer hover:bg-white dark:hover:bg-slate-900 transition-colors"
                                        >
                                            <option value="COLABORADOR">Colaborador</option>
                                            <option value="DIRECTOR">Director (Admin)</option>
                                        </select>
                                        <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
                                            <i className="fas fa-chevron-down text-xs"></i>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <label className="block text-sm font-bold text-slate-700 dark:text-slate-300 mb-2">Estado</label>
                                    <div className="relative">
                                        <select
                                            value={editingUser.activo ? 'true' : 'false'}
                                            onChange={(e) => setEditingUser({ ...editingUser, activo: e.target.value === 'true' })}
                                            className="w-full px-4 py-3.5 rounded-xl bg-slate-50 dark:bg-slate-900/50 border border-slate-200 dark:border-slate-700 focus:ring-2 focus:ring-blue-500 outline-none text-slate-800 dark:text-white appearance-none cursor-pointer hover:bg-white dark:hover:bg-slate-900 transition-colors"
                                        >
                                            <option value="true">Activo</option>
                                            <option value="false">Inactivo</option>
                                        </select>
                                        <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none text-slate-500">
                                            <i className="fas fa-chevron-down text-xs"></i>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div className="flex justify-end gap-3 mt-6">
                                <button
                                    type="button"
                                    onClick={() => setEditingUser(null)}
                                    className="px-4 py-2 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 rounded-xl font-medium"
                                >
                                    Cancelar
                                </button>
                                <button
                                    type="submit"
                                    className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl font-bold shadow-lg shadow-blue-500/30"
                                >
                                    Guardar Cambios
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            {/* PIN Verification Modal */}
            <PinVerificationModal
                isOpen={isPinModalOpen}
                onClose={() => {
                    setIsPinModalOpen(false);
                    setPendingAction(null);
                }}
                onVerify={verifyPin}
                title="Verificación de Seguridad"
                description="Para continuar con esta operación, ingresa tu PIN de 6 dígitos"
            />

            {/* Add User Modal */}
            <AddUserModal
                isOpen={isAddModalOpen}
                onClose={() => setIsAddModalOpen(false)}
                onSuccess={handleUserAdded}
            />

            {/* Delete User Modal */}
            <DeleteUserModal
                isOpen={isDeleteModalOpen}
                onClose={() => {
                    setIsDeleteModalOpen(false);
                    setUserToDelete(null);
                }}
                user={userToDelete}
                onSuccess={handleUserDeleted}
            />
        </div>
    );
}
