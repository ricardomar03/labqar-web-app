from __future__ import absolute_import
from __future__ import unicode_literals

import datetime
import io
from PIL import Image

from .models import *
from celery import shared_task

# Not Implemented
@shared_task
def inserir_alarmes(alr_id, alr_nome, alr_enable, alr_tipo, alr_rede, can_id, alr_limite_min, alr_limite_max, alr_estado, alr_intervalo_validade, alr_log_only, est_id):
    return

# Not Implemented
@shared_task
def inserir_alarmes_operadores(alr_id, ope_id, alr_prioridade):
    return

# Not Implemented
@shared_task
def inserir_alertas(ale_id, can_id, ale_limite, ale_enable, ale_mensagem, ale_intervalo_validade, ale_tipo_media, ale_log_only):
    return

# Not Implemented
@shared_task
def inserir_alertes_operadores(ale_id, ope_id):
    return

# Not Implemented
@shared_task
def inserir_area(area_id, are_name, are_url, are_login, are_password, are_area_id, are_dias_semanas, are_hora_actl, are_hora_calc, are_perc_validacao, are_data_indentr, are_data_dadentr, are_tipo, are_entr_dados, are_entr_dados_val, are_entr_inddices, are_entr_ciclica, are_entr_hora, are_entr_intervalo):
    return

# Not Implemented
@shared_task
def inserir_area_estacao(are_id, est_id):
    return

# Not Implemented
@shared_task
def inserir_campanha(cam_id, est_id, cam_nome, cam_local, cam_coord_lat, cam_coord_long, cam_coord_alt, cam_data_inicio, cam_data_fim, cam_foto1, cam_foto1_cx, cam_foto1_cy, cam_foto2, cam_foto2_cx, cam_foto2_cy, cam_projecto, cam_observacpes):
    return

@shared_task
def inserir_canal(can_id, uni_id, par_id, can_num_estacao, can_num_unidade, can_unidade_medida, can_conv_med_mul, can_conv_med_add, can_min_medida, can_max_medida, can_min_alarme,
                  can_max_alarme, can_validacao, can_suspenso, can_background, can_coeficiente, can_num_monit, ual_meteo, ual_sin_cmd, ual_slope, ual_y0, ual_nome, sam_ganho, sam_sin_alarme,
                  sam_sin_zero, sam_sin_max, sam_cmd_zero, sam_cmd_max, vir_formula, uar_tipo, uar_calculo, uar_num_entrada, can_reg_eventos, can_addr_eventos, can_acumula_eventos):
    novoCanal = Canal(can_id, uni_id, par_id, can_num_estacao, can_num_unidade, can_unidade_medida, can_conv_med_mul, can_conv_med_add, can_min_medida, can_max_medida, can_min_alarme,
                      can_max_alarme, can_validacao, can_suspenso, can_background, can_coeficiente, can_num_monit, ual_meteo, ual_sin_cmd, ual_slope, ual_y0, ual_nome, sam_ganho,
                      sam_sin_alarme, sam_sin_zero, sam_sin_max, sam_cmd_zero, sam_cmd_max, vir_formula, uar_tipo, uar_calculo, uar_num_entrada, can_reg_eventos, can_addr_eventos,
                      can_acumula_eventos)
    novoCanal.save()

# Not Implemented
@shared_task
def inserir_categoria(cat_id, cat_nome):
    return

# Not Implemented
@shared_task
def inserir_caudal(cdl_id,  can_id, cdl_nivel, cdl_caudal):
    return

# Not Implemented
@shared_task
def inserir_config(cfg_nome, cfg_valor):
    return

@shared_task
def inserir_dados(dad_id, est_id, cam_id, dad_data, dad_1med, dad_1stat, dad_2med, dad_2stat, dad_3med, dad_3stat, dad_4med, dad_4stat, dad_5med, dad_5stat, dad_6med, dad_6stat,
                  dad_7med, dad_7stat, dad_8med, dad_8stat, dad_9med, dad_9stat, dad_10med, dad_10stat, dad_11med, dad_11stat, dad_12med, dad_12stat, dad_13med, dad_13stat,
                  dad_14med, dad_14stat, dad_15med, dad_15stat, dad_16med, dad_16stat, dad_17med, dad_17stat, dad_18med, dad_18stat, dad_19med, dad_19stat,dad_20med, dad_20stat,
                  dad_p_aquisicao):
    if dad_data:
        dad_data = datetime.datetime.strptime(dad_data, "%Y-%m-%dT%H:%M:%S")
    else:
        dad_data = None
    novosDados = Dados(dad_id, est_id, cam_id, dad_data, dad_1med, dad_1stat, dad_2med, dad_2stat, dad_3med, dad_3stat, dad_4med, dad_4stat, dad_5med, dad_5stat, dad_6med, dad_6stat,
                       dad_7med, dad_7stat, dad_8med, dad_8stat, dad_9med, dad_9stat, dad_10med, dad_10stat, dad_11med, dad_11stat, dad_12med, dad_12stat, dad_13med, dad_13stat,
                       dad_14med, dad_14stat, dad_15med, dad_15stat, dad_16med, dad_16stat, dad_17med, dad_17stat, dad_18med, dad_18stat, dad_19med, dad_19stat,dad_20med, dad_20stat,
                       dad_p_aquisicao)
    novosDados.save()

# Not Implemented
@shared_task
def inserir_dados_caudal(dc_id, dad_id, dc_canal, dc_haste, dc_distancias, dc_alturas, dc_velocidades):
    return

# Not Implemented
@shared_task
def inserir_dados_originais(do_id, est_id, do_data, do_canal, do_valor, do_estado):
    return

# Not Implemented
@shared_task
def inserir_entrega(ent_id, are_id, ent_hora, ent_dias_semana):
    return

@shared_task
def inserir_estacao(est_id, map_id, red_id, est_nome, est_abreviatura, est_codigo, est_instituicao, est_pos_x, est_pos_y, est_local, est_data_instal, est_tipo_ligacao, est_telefone,
                    est_central_telef, est_indicativo, est_ultima_revisao, est_foto, est_obs, est_alarme_a, est_tel_alarme_a, est_alarme_b, est_tel_alarme_b, est_alarme_c, est_tel_alarme_c,
                    est_num_tent, est_atraso_tent, est_p_aq_normal, est_p_aq_alarme, est_perc_validacao, est_num_canais_activ, est_mascara, est_data_validacao, est_comunicacao, est_modem_init,
                    est_modem_dial, est_template, est_relogio_sinc, est_autonomia, est_meteo_est_id, est_meteo_vel_id, est_meteo_dir_id, est_meteo_used, est_auto_validacao,
                    cam_id, est_porta_serie, est_tipo, est_activa, est_data_ult_act):
    if est_data_instal:
        est_data_instal = datetime.datetime.strptime(est_data_instal, "%Y-%m-%dT%H:%M:%S")
    else:
        est_data_instal = None
    if est_ultima_revisao:
        est_ultima_revisao = datetime.datetime.strptime(est_ultima_revisao, "%Y-%m-%dT%H:%M:%S")
    else:
        est_ultima_revisao = None
    if est_data_validacao:
        est_data_validacao = datetime.datetime.strptime(est_data_validacao, "%Y-%m-%dT%H:%M:%S")
    else:
        est_data_validacao = None
    if est_data_ult_act:
        est_data_ult_act = datetime.datetime.strptime(est_data_ult_act, "%Y-%m-%dT%H:%M:%S")
    else:
        est_data_ult_act = None
    novaEstacao = Estacao(est_id, map_id, red_id, est_nome, est_abreviatura, est_codigo, est_instituicao, est_pos_x, est_pos_y, est_local, est_data_instal, est_tipo_ligacao, est_telefone,
                           est_central_telef, est_indicativo, est_ultima_revisao, None, est_obs, est_alarme_a, est_tel_alarme_a, est_alarme_b, est_tel_alarme_b, est_alarme_c,
                           est_tel_alarme_c, est_num_tent, est_atraso_tent, est_p_aq_normal, est_p_aq_alarme, est_perc_validacao, est_num_canais_activ, est_mascara, est_data_validacao,
                           est_comunicacao, est_modem_init, est_modem_dial, est_template, est_relogio_sinc, est_autonomia, est_meteo_est_id, est_meteo_vel_id, est_meteo_dir_id,
                           est_meteo_used, est_auto_validacao, cam_id, est_porta_serie, est_tipo, est_activa, est_data_ult_act)
    novaEstacao.save()

@shared_task
def inserir_estado(est_id, est_data, est_1med, est_1mode, est_1valido, est_1alarme, est_2med, est_2mode, est_2valido, est_2alarme, est_3med, est_3mode, est_3valido, est_3alarme,
                   est_4med, est_4mode, est_4valido, est_4alarme, est_5med, est_5mode, est_5valido, est_5alarme, est_6med, est_6mode, est_6valido, est_6alarme, est_7med, est_7mode,
                   est_7valido, est_7alarme, est_8med, est_8mode, est_8valido, est_8alarme, est_9med, est_9mode, est_9valido, est_9alarme, est_10med, est_10mode, est_10valido, est_10alarme,
                   est_11med, est_11mode, est_11valido, est_11alarme, est_12med, est_12mode, est_12valido, est_12alarme, est_13med, est_13mode, est_13valido, est_13alarme, est_14med,
                   est_14mode, est_14valido, est_14alarme, est_15med, est_15mode, est_15valido, est_15alarme, est_16med, est_16mode, est_16valido, est_16alarme, est_17med, est_17mode,
                   est_17valido, est_17alarme, est_18med, est_18mode, est_18valido, est_18alarme, est_19med, est_19mode, est_19valido, est_19alarme, est_20med, est_20mode, est_20valido,
                   est_20alarme):
    if est_data:
        est_data = datetime.datetime.strptime(est_data, "%Y-%m-%dT%H:%M:%S")
    else:
        est_data = None
    novoEstado = Estado(est_id, est_data, est_1med, est_1mode, est_1valido, est_1alarme, est_2med, est_2mode, est_2valido, est_2alarme, est_3med, est_3mode, est_3valido, est_3alarme,
                        est_4med, est_4mode, est_4valido, est_4alarme, est_5med, est_5mode, est_5valido, est_5alarme, est_6med, est_6mode, est_6valido, est_6alarme, est_7med, est_7mode,
                        est_7valido, est_7alarme, est_8med, est_8mode, est_8valido, est_8alarme, est_9med, est_9mode, est_9valido, est_9alarme, est_10med, est_10mode, est_10valido,
                        est_10alarme, est_11med, est_11mode, est_11valido, est_11alarme, est_12med, est_12mode, est_12valido, est_12alarme, est_13med, est_13mode, est_13valido, est_13alarme,
                        est_14med, est_14mode, est_14valido, est_14alarme, est_15med, est_15mode, est_15valido, est_15alarme, est_16med, est_16mode, est_16valido, est_16alarme, est_17med,
                        est_17mode, est_17valido, est_17alarme, est_18med, est_18mode, est_18valido, est_18alarme, est_19med, est_19mode, est_19valido, est_19alarme, est_20med, est_20mode,
                        est_20valido, est_20alarme)
    novoEstado.save()

@shared_task
def inserir_estado_interno(uni_id, est_data, est_1nome, est1_unidmed, est_1valor, est_1modo, est_1valido, est_2nome, est_2unidmed, est_2valor, est_2modo, est_2valido, est_3nome,
                           est_3unidmed, est_3valor, est_3modo, est_3valido, est_4nome, est_4unidmed, est_4valor, est_4modo, est_4valido, est_5nome, est_5unidmed, est_5valor,
                           est_5modo, est_5valido, est_6nome, est_6unidmed, est_6valor, est_6modo, est_6valido, est_7nome, est_7unidmed, est_7valor, est_7modo, est_7valido, est_8nome,
                           est_8unidmed, est_8valor, est_8modo, est_8valido, est_9nome, est_9unidmed, est_9valor, est_9modo, est_9valido, est_10nome, est_10unidmed, est_10valor,
                           est_10modo, est_10valido, est_11nome, est_11unidmed, est_11valor, est_11modo, est_11valido, est_12nome, est_12unidmed, est_12valor, est_12modo, est_12valido,
                           est_13nome, est_13unidmed, est_13valor, est_13modo, est_13valido, est_14nome, est_14unidmed, est_14valor, est_14modo, est_14valido, est_15nome, est_15unidmed,
                           est_15valor, est_15modo, est_15valido, est_16nome, est_16unidmed, est_16valor, est_16modo, est_16valido):
    if est_data:
        est_data = datetime.datetime.strptime(est_data, "%Y-%m-%dT%H:%M:%S")
    else:
        est_data = None
    novoEstado_Interno = EstadoInterno(uni_id, est_data, est_1nome, est1_unidmed, est_1valor, est_1modo, est_1valido, est_2nome, est_2unidmed, est_2valor, est_2modo, est_2valido,
                                       est_3nome, est_3unidmed, est_3valor, est_3modo, est_3valido, est_4nome, est_4unidmed, est_4valor, est_4modo, est_4valido, est_5nome, est_5unidmed,
                                       est_5valor, est_5modo, est_5valido, est_6nome, est_6unidmed, est_6valor, est_6modo, est_6valido, est_7nome, est_7unidmed, est_7valor, est_7modo,
                                       est_7valido, est_8nome, est_8unidmed, est_8valor, est_8modo, est_8valido, est_9nome, est_9unidmed, est_9valor, est_9modo, est_9valido, est_10nome,
                                       est_10unidmed, est_10valor, est_10modo, est_10valido, est_11nome, est_11unidmed, est_11valor, est_11modo, est_11valido, est_12nome, est_12unidmed,
                                       est_12valor, est_12modo, est_12valido, est_13nome, est_13unidmed, est_13valor, est_13modo, est_13valido, est_14nome, est_14unidmed, est_14valor,
                                       est_14modo, est_14valido, est_15nome, est_15unidmed, est_15valor, est_15modo, est_15valido, est_16nome, est_16unidmed, est_16valor, est_16modo,
                                       est_16valido)
    novoEstado_Interno.save()

# Not Implemented
@shared_task
def inseir_eventos(evt_id, est_id, evt_canal, evt_data, evt_val, evt_stat):
    return

# Not Implemented
@shared_task
def inserir_indice(ind_id, are_id, ind_data, ind_indice, ind_co, ind_co_val, ind_no2, ind_no2_val, ind_o3, ind_o3_val, ind_pm10, ind_pm_10_val, ind_so2, ind_so2_val, ind_val, ind_poluente):
    return

# Not Implemented
@shared_task
def inserir_invalidacao(inv_id, est_id, ope_id, inv_data, inv_canal, inv_razao, inv_intervalo_inicio, inv_intervalo_fim, inv_obs):
    return

# Not Implemented
@shared_task
def inserir_limites(lim_id, par_id, lim_ano, lim_mau_min, lim_fraco_min, lim_fraco_max, lim_medio_min, lim_medio_max, lim_bom_min, lim_bom_max, lim_mtobom_min, lim_mtobom_max):
    return

# Not Implemented
@shared_task
def inserir_log_alarmes(lalr_id, alr_id, lalr_data, lalr_valor, lalr_aceite, ope_id, lalr_obs, lalr_resolvido, lalr_expirado, lalr_recebido):
    return

# Not Implemented
@shared_task
def inserir_log_alertas(lale_id, ale_id, lale_data, late_limite_configurado, late_valor_encontrado):
    return

# Not Implemented
@shared_task
def inserir_log_mesgs_rx_tx(msg_id, ope_id, msg_data, msg_tipo, msg_mensagem):
    return

@shared_task
def inserir_mapa(map_id, map_nome, map_ficheiro):
    novoMapa = Mapa(map_id, map_nome, map_ficheiro)
    novoMapa.save()

# Not Implemented
@shared_task
def inserir_operadores(ope_id, ope_nome, ope_nome_completo, ope_telemovel, ope_observacoes, ope_atraso, ope_email, ope_dias_semana, ope_telemovel_on, ope_password, ope_permissoes):
    return

@shared_task
def inserir_parametro(par_id, cat_id, par_nome, par_nome_completo, par_codigo, par_unidade_armaz, par_unidade_apresent, par_conv_mul, par_conv_add, par_casas_decimais, par_limiar, par_limite, par_perc_validacao_hora, par_perc_validacao_dia, par_media_tipo, par_media_intervalo, par_visivil, par_min_alarme, par_max_alarme, par_limite_media, par_tipo):
    novoParametro = Parametro(par_id, cat_id, par_nome, par_nome_completo, par_codigo, par_unidade_armaz, par_unidade_apresent, par_conv_mul, par_conv_add, par_casas_decimais, par_limiar, par_limite, par_perc_validacao_hora, par_perc_validacao_dia, par_media_tipo, par_media_intervalo, par_visivil, par_min_alarme, par_max_alarme, par_limite_media, par_tipo)
    novoParametro.save()

@shared_task
def inserir_recolha(rec_id, est_id, rec_hora, rec_dias_semana):
    novaRecolha = Recolha(rec_id, est_id, rec_hora, rec_dias_semana)
    novaRecolha.save()


@shared_task
def inserir_rede(red_id, red_descricao):
    novaRede = Rede(red_id, red_descricao)
    novaRede.save()

# Not Implemented
@shared_task
def inserir_relatorio(rel_id, est_id, rel_registo, rel_data, rel_tipo, rel_info, rel_dado):
    return

@shared_task
def inserir_unidade(uni_id, est_id, uni_tipo, uni_num_serie, uni_nome, uni_ual_lres, uni_ual_hres, uni_dt_programa, uni_ual_prodid, uni_ual_majver, uni_ual_minver, uni_ual_revver,
                    uni_sam_calib_zero, uni_sam_calib_max, uni_sam_sinc_calibh, uni_sam_sinc_calibm, uni_sam_ciclo_calib, uni_asm_endereco, uni_asm_offset, uni_asm_gama, uni_asm_tempo_resp,
                    uni_asm_unidade, uni_asm_calib_zero_ref, uni_asm_calib_zero, uni_asm_calib_auto, uni_asm_calib_max, uni_asm_dur_zero, uni_asm_dur_max, uni_asm_span, uni_asm_banco,
                    uni_versao, uni_modelo, uni_suspenso, uni_dt_recolha, uni_tea_tavrg, uni_tea_ctemp, uni_tea_cpres, uni_asm_modo, uni_ccr_nloca_amostra, uni_ccr_nloca_total, uni_dtl_password,
                    uni_obs_intervalo_s, uni_obs_intervalo_p, uni_obs_intervalo_q, uni_obs_bateria, uni_obs_cartridge, uni_obs_apaga_dados, uni_ccr_nloca_eventos, uni_ccr_nloca_total_eventos):
    if uni_dt_programa:
        uni_dt_programa = datetime.datetime.strptime(uni_dt_programa, "%Y-%m-%dT%H:%M:%S")
    else:
        uni_dt_programa = None
    if uni_dt_recolha:
        uni_dt_recolha = datetime.datetime.strptime(uni_dt_recolha, "%Y-%m-%dT%H:%M:%S")
    else:
        uni_dt_recolha = None
    novaUnidade = Unidade(uni_id, est_id, uni_tipo, uni_num_serie, uni_nome, uni_ual_lres, uni_ual_hres, uni_dt_programa, uni_ual_prodid, uni_ual_majver, uni_ual_minver, uni_ual_revver,
                          uni_sam_calib_zero, uni_sam_calib_max, uni_sam_sinc_calibh, uni_sam_sinc_calibm, uni_sam_ciclo_calib, uni_asm_endereco, uni_asm_offset, uni_asm_gama,
                          uni_asm_tempo_resp, uni_asm_unidade, uni_asm_calib_zero_ref, uni_asm_calib_zero, uni_asm_calib_auto, uni_asm_calib_max, uni_asm_dur_zero, uni_asm_dur_max,
                          uni_asm_span, uni_asm_banco, uni_versao, uni_modelo, uni_suspenso, uni_dt_recolha, uni_tea_tavrg, uni_tea_ctemp, uni_tea_cpres, uni_asm_modo, uni_ccr_nloca_amostra,
                          uni_ccr_nloca_total, uni_dtl_password, uni_obs_intervalo_s, uni_obs_intervalo_p, uni_obs_intervalo_q, uni_obs_bateria, uni_obs_cartridge, uni_obs_apaga_dados,
                          uni_ccr_nloca_eventos, uni_ccr_nloca_total_eventos)
    novaUnidade.save()