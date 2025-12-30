'use client';

import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { LogOut, X } from 'lucide-react';
import { cn } from '@/lib/utils';
import { Button } from '@/components/ui/button';

export function LogoutModal({
    open,
    onOpenChange,
    onConfirm
}: {
    open: boolean;
    onOpenChange: (open: boolean) => void;
    onConfirm: () => void;
}) {
    return (
        <DialogPrimitive.Root open={open} onOpenChange={onOpenChange}>
            <DialogPrimitive.Portal>
                {/* Backdrop with blur and fade animation */}
                <DialogPrimitive.Overlay
                    className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0"
                />

                {/* Modal Content with zoom/slide animation */}
                <DialogPrimitive.Content
                    className={cn(
                        "fixed left-[50%] top-[50%] z-50 grid w-full max-w-sm translate-x-[-50%] translate-y-[-50%] gap-6 border border-gray-100 bg-white p-8 shadow-2xl duration-300",
                        "data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%]",
                        "rounded-[2rem]"
                    )}
                >
                    <div className="flex flex-col items-center text-center gap-5 pt-2">
                        {/* Icon Circle */}
                        <div className="h-20 w-20 bg-red-50 rounded-full flex items-center justify-center mb-1 animate-in zoom-in spin-in-12 duration-700 shadow-sm ring-4 ring-red-50/50">
                            <LogOut className="h-9 w-9 text-red-500 stroke-[2.5px] ml-1" />
                        </div>

                        <div className="space-y-3">
                            <DialogPrimitive.Title className="text-2xl font-black tracking-tight text-[#0F2C4A]">
                                ¿Cerrar Sesión?
                            </DialogPrimitive.Title>
                            <DialogPrimitive.Description className="text-[15px] text-gray-500 max-w-[280px] mx-auto leading-relaxed font-medium">
                                ¿Estás seguro que deseas salir del sistema? Tendrás que volver a ingresar tus credenciales.
                            </DialogPrimitive.Description>
                        </div>
                    </div>

                    <div className="flex flex-col-reverse sm:flex-row sm:justify-center gap-3 w-full mt-2">
                        <Button
                            variant="outline"
                            onClick={() => onOpenChange(false)}
                            className="w-full sm:w-auto flex-1 rounded-xl h-12 border-gray-200 text-gray-600 hover:bg-gray-50 hover:text-gray-900 font-bold transition-all hover:border-gray-300"
                        >
                            Cancelar
                        </Button>
                        <Button
                            variant="destructive"
                            onClick={onConfirm}
                            className="w-full sm:w-auto flex-1 rounded-xl h-12 bg-[#DC2626] hover:bg-[#B91C1C] shadow-lg shadow-red-500/30 transition-all font-bold hover:scale-[1.02] active:scale-[0.98]"
                        >
                            Cerrar Sesión
                        </Button>
                    </div>
                </DialogPrimitive.Content>
            </DialogPrimitive.Portal>
        </DialogPrimitive.Root>
    );
}
