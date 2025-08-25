import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface EmpathicHelpDialogProps {
  open: boolean;
  onClose: () => void;
  errorContext: {
    formId: string;
    errorType: string;
    errorCount: number;
  };
}

function EmpathicHelpDialog({ open, onClose, errorContext }: EmpathicHelpDialogProps) {
  const safeContext = errorContext || { formId: '', errorType: '', errorCount: 0 };
  
  return (
    <AnimatePresence>
      {open && (
        <>
          {/* Backdrop */}
          <motion.div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          
          {/* Dialog */}
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
            <motion.div
              className="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6"
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              transition={{ duration: 0.3, ease: "easeOut" }}
            >
              {/* Header */}
              <div className="mb-6">
                <div className="flex items-center gap-3 mb-2">
                  <div className="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                    <span className="text-blue-600 text-lg">💡</span>
                  </div>
                  <h2 className="text-xl font-bold text-gray-900">Ajuda Inteligente</h2>
                </div>
                <p className="text-gray-600 text-sm">
                  Identificamos um problema e estamos aqui para ajudar!
                </p>
              </div>

              {/* Content */}
              <div className="space-y-4 mb-6">
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <span className="text-red-500 text-lg">⚠️</span>
                    <div>
                      <p className="text-red-800 font-medium">
                        Erro detectado: <span className="font-bold">{safeContext.errorType}</span>
                      </p>
                      <p className="text-red-700 text-sm mt-1">
                        Formulário: <span className="font-mono bg-red-100 px-2 py-1 rounded">{safeContext.formId}</span>
                      </p>
                    </div>
                  </div>
                </div>

                {safeContext.errorCount > 1 && (
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                    <div className="flex items-center gap-3">
                      <span className="text-yellow-600 text-lg">🔄</span>
                      <p className="text-yellow-800">
                        Este erro ocorreu <span className="font-bold">{safeContext.errorCount} vezes</span> consecutivas.
                      </p>
                    </div>
                  </div>
                )}

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <div className="flex items-start gap-3">
                    <span className="text-blue-600 text-lg">💬</span>
                    <div>
                      <p className="text-blue-800 font-medium">Precisa de ajuda?</p>
                      <p className="text-blue-700 text-sm mt-1">
                        Consulte nossa documentação ou entre em contato com o suporte técnico.
                      </p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-3">
                <button
                  onClick={onClose}
                  className="flex-1 px-4 py-2 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors font-medium"
                >
                  Fechar
                </button>
                <button
                  onClick={onClose}
                  className="flex-1 px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors font-medium"
                >
                  Ver Dicas
                </button>
              </div>
            </motion.div>
          </div>
        </>
      )}
    </AnimatePresence>
  );
}

export default EmpathicHelpDialog;
