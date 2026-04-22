import pygame

class Ciclos:
    def __init__(self):
        self.tempo_ficticio = 0.0  # Tempo total pausável em ms (para dias)
        self.tempo_decorrido_ciclo = 0.0
        self.duracao_dia = 18000  # minutos em ms
        self.duracao_noite = 18000  # minutos em ms
        self.estado_atual = 'dia'
        self.progresso = 0.0
        self.dia_atual = 1
        self._duracao_atual = self.duracao_dia
        self.cor_ceu_dia = (135, 206, 235)
        self.cor_ceu_noite = (25, 25, 112)
        self.cor_ceu = self.cor_ceu_dia

    def update(self, dt, paused):
        if paused:
            return

        self.tempo_ficticio += dt
        hora_decimal = self.get_hora_decimal()
        
        # Transições precisas: amanhecer 6h (fade até 7h dia total), anoitecer 18h (fade até 19h noite total)
        if 6 <= hora_decimal < 7:
            prog = (hora_decimal - 6) / 1.0  # 0 (6h escuro) → 1 (7h claro)
            self.estado_atual = 'dia'
            self.cor_ceu = self.cor_ceu_dia
            self.progresso = 1 - prog  # Inverso para fade in
        elif 7 <= hora_decimal < 18:
            self.estado_atual = 'dia'
            self.cor_ceu = self.cor_ceu_dia
            self.progresso = 0.0
        elif 18 <= hora_decimal < 19:
            prog = (hora_decimal - 18) / 1.0  # 0 (18h claro) → 1 (19h escuro)
            self.estado_atual = 'noite'
            self.cor_ceu = self.cor_ceu_noite
            self.progresso = prog
        else:  # 19h-6h noite total ou antes 6h
            self.estado_atual = 'noite'
            self.cor_ceu = self.cor_ceu_noite
            self.progresso = 1.0

    def get_hora_decimal(self):
        ciclo_total = self.duracao_dia + self.duracao_noite
        fracao_dia = (self.tempo_ficticio % ciclo_total) / ciclo_total
        return fracao_dia * 24



    def _alternar_ciclo(self):
        if self.estado_atual == 'dia':
            self.estado_atual = 'noite'
            self._duracao_atual = self.duracao_noite
            self.cor_ceu = self.cor_ceu_noite
        else:
            self.estado_atual = 'dia'
            self._duracao_atual = self.duracao_dia
            self.cor_ceu = self.cor_ceu_dia
            self.dia_atual += 1

    def get_estado(self):
        return self.estado_atual

    def get_progresso(self):
        return self.progresso

    def get_cor_ceu(self):
        return self.cor_ceu

    def is_noite(self):
        return self.estado_atual == 'noite'

    def get_alpha_sombra(self):
        return self.progresso * 0.7 if self.is_noite() else 0.0

    def get_tempo_hh_mm(self):
        ciclo_total = self.duracao_dia + self.duracao_noite
        fracao_dia = self.tempo_ficticio / ciclo_total
        dias_totais = int(fracao_dia)
        minutos_do_dia = (fracao_dia % 1) * 24 * 60
        horas = int(minutos_do_dia // 60)
        minutos = int(minutos_do_dia % 60)
        self.dia_atual = dias_totais + 1
        return f"{horas:02d}:{minutos:02d}"

    def get_save_data(self):
        return {
            'tempo_ficticio': self.tempo_ficticio,
            'dia_atual': self.dia_atual,
            'estado_atual': self.estado_atual,
            'tempo_decorrido_ciclo': self.tempo_decorrido_ciclo
        }

    def load_data(self, data):
        self.tempo_ficticio = data.get('tempo_ficticio', 0.0)
        self.dia_atual = data.get('dia_atual', 1)
        self.estado_atual = data.get('estado_atual', 'dia')
        self.tempo_decorrido_ciclo = data.get('tempo_decorrido_ciclo', 0.0)
        self._duracao_atual = self.duracao_noite if self.estado_atual == 'noite' else self.duracao_dia
        self.progresso = self.tempo_decorrido_ciclo / self._duracao_atual
        self.cor_ceu = self.cor_ceu_noite if self.estado_atual == 'noite' else self.cor_ceu_dia

