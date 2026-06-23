# Diagramas — Entrega 3

Diagramas em Mermaid para visualização e captura de tela. Para renderizar:

- **GitHub:** abre nativamente este arquivo já renderizado.
- **VS Code:** instale "Markdown Preview Mermaid Support" e abra o preview.
- **Online:** copie cada bloco para <https://mermaid.live>.

---

## UC02 — Executar Timing Drill (Pedro)

### Diagrama de Atividades — UC02

```mermaid
flowchart TD
    Start([Início]) --> A1[Sistema: exibir formulário de configuração]
    A1 --> A2[Praticante: informar duração, intervalos e técnica]
    A2 --> A3[Praticante: acionar início]
    A3 --> D1{Configuração válida?}
    D1 -- "[não]" --> E1[Sistema: exibir mensagem de erro]
    E1 --> A1
    D1 -- "[sim]" --> A4[Sistema: exibir contagem regressiva com beeps]
    A4 --> A5[Sistema: iniciar sessão e sortear próximo estímulo]
    A5 --> A6[Sistema: avançar um segundo]
    A6 --> D2{Duração total atingida?}
    D2 -- "[sim]" --> A7[Sistema: sinalizar encerramento]
    A7 --> A8[Sistema: anunciar fim da sessão]
    A8 --> A9[Sistema: retornar ao formulário]
    A9 --> End([Fim])
    D2 -- "[não]" --> D3{Sessão pausada?}
    D3 -- "[sim]" --> A6
    D3 -- "[não]" --> D4{Instante de estímulo atingido?}
    D4 -- "[sim]" --> A10[Sistema: emitir estímulo — beep, anúncio e destaque]
    A10 --> A11[Sistema: sortear próximo estímulo]
    A11 --> A6
    D4 -- "[não]" --> A6
```

### Diagrama de Sequência — UC02

```mermaid
sequenceDiagram
    actor Pr as :Praticante
    participant Pg as :TimingDrillPage
    participant Cfg as :TimingDrillConfig
    participant Se as :TimingDrillSession
    participant Tm as :DrillTimer
    participant Au as :AudioEngine
    participant An as :Announcer

    Pr->>Pg: preencher_campos()
    Pr->>Pg: click(btn-start)
    Pg->>Cfg: new(duration, min, max, technique)
    Pg->>Cfg: validate()

    alt configuração inválida
        Cfg-->>Pg: ValueError
        Pg->>Pr: mostrar_erro()
    else configuração válida
        Pg->>Se: new(config)
        Pg->>Se: on_event(handle_event)
        Pg->>Tm: new(session, update, countdown, audio)
        Pg->>Tm: start()
        Tm->>Au: play_countdown_tick_signal() (x3)
        Tm->>Se: start()
        Tm->>Au: play_countdown_end_signal()

        loop a cada 1s até SESSION_END
            Tm->>Se: tick()
            Se->>Se: _on_tick()
            alt elapsed >= total_duration
                Se->>Pg: emit(SESSION_END)
                Pg->>Au: play_end_signal()
                Pg->>An: announce("Fim da sessão")
                Pg->>Pr: voltar_ao_formulário()
            else elapsed >= next_stimulus_at
                Se->>Pg: emit(STIMULUS, {technique})
                Pg->>Au: play_start_signal()
                Pg->>An: announce(technique)
                Se->>Se: _schedule_next()
            end
        end
    end

    opt usuário solicita pausa
        Pr->>Pg: click(btn-pause)
        Pg->>Tm: pause()
        Tm->>Se: pause()
    end

    opt usuário solicita parar
        Pr->>Pg: click(btn-stop)
        Pg->>Tm: stop()
        Tm->>Se: stop()
    end
```

---

## UC04 — Executar Footwork Drill (Vitor)

### Diagrama de Atividades — UC04

```mermaid
flowchart TD
    Start([Início]) --> A0[Praticante: acessar página]
    A0 --> D0{Biblioteca de movimentações vazia?}
    D0 -- "[sim]" --> A0a[Sistema: exibir estado vazio e atalho para gerenciar movimentações]
    A0a --> End([Fim])
    D0 -- "[não]" --> A1[Sistema: exibir formulário com movimentações]
    A1 --> A2[Praticante: selecionar movimentações e preencher parâmetros]
    A2 --> A3[Praticante: acionar início]
    A3 --> D1{Seleção e parâmetros válidos?}
    D1 -- "[não]" --> E1[Sistema: exibir mensagem de erro]
    E1 --> A1
    D1 -- "[sim]" --> A4[Sistema: exibir contagem regressiva com beeps]
    A4 --> A5[Sistema: iniciar sessão]
    A5 --> A6[Sistema: sortear primeira movimentação, anunciar e emitir beep]
    A6 --> A7[Sistema: agendar próximo instante de chamada]
    A7 --> A8[Sistema: avançar um segundo]
    A8 --> D2{Duração total atingida?}
    D2 -- "[sim]" --> A9[Sistema: sinalizar encerramento]
    A9 --> A10[Sistema: anunciar fim da sessão]
    A10 --> A11[Sistema: retornar ao formulário]
    A11 --> End
    D2 -- "[não]" --> D3{Sessão pausada?}
    D3 -- "[sim]" --> A8
    D3 -- "[não]" --> D4{Instante de chamada atingido?}
    D4 -- "[sim]" --> A12[Sistema: sortear movimentação aleatória]
    A12 --> A13[Sistema: emitir chamada — beep, anúncio e destaque]
    A13 --> A14[Sistema: agendar próximo instante de chamada]
    A14 --> A8
    D4 -- "[não]" --> A8
```

### Diagrama de Sequência — UC04

```mermaid
sequenceDiagram
    actor Pr as :Praticante
    participant Pg as :FootworkDrillPage
    participant Lib as :FootworkMoveLibrary
    participant Cfg as :FootworkDrillConfig
    participant Se as :FootworkDrillSession
    participant Tm as :DrillTimer
    participant Au as :AudioEngine
    participant An as :Announcer

    Pr->>Pg: abrir_pagina()
    Pg->>Lib: list_all()
    Lib-->>Pg: moves[]

    alt biblioteca vazia
        Pg->>Pr: exibir_estado_vazio()
    else biblioteca não vazia
        Pg->>Pr: exibir_formulario(moves)
        Pr->>Pg: selecionar_e_preencher()
        Pr->>Pg: click(btn-start)
        Pg->>Cfg: new(selecionados, min, max, duration)
        Pg->>Cfg: validate()

        alt config inválida
            Cfg-->>Pg: ValueError
            Pg->>Pr: mostrar_erro()
        else config válida
            Pg->>Se: new(config)
            Pg->>Se: on_event(handle_event)
            Pg->>Tm: new(session, update, countdown, audio)
            Pg->>Tm: start()
            Tm->>Au: play_countdown_tick_signal() (x3)
            Tm->>Se: start()
            Se->>Se: _call_move()
            Se->>Pg: emit(MOVE_CALL, {move})
            Pg->>Au: play_start_signal()
            Pg->>An: announce(move.name)
            Se->>Se: _schedule_next()
            Tm->>Au: play_countdown_end_signal()

            loop a cada 1s até SESSION_END
                Tm->>Se: tick()
                Se->>Se: _on_tick()
                alt elapsed >= total_duration
                    Se->>Pg: emit(SESSION_END)
                    Pg->>Au: play_end_signal()
                    Pg->>An: announce("Fim da sessão")
                    Pg->>Pr: voltar_ao_formulário()
                else elapsed >= next_call_at
                    Se->>Se: _call_move()
                    Se->>Pg: emit(MOVE_CALL, {move})
                    Pg->>Au: play_start_signal()
                    Pg->>An: announce(move.name)
                    Se->>Se: _schedule_next()
                end
            end
        end
    end

    opt usuário solicita pausa
        Pr->>Pg: click(btn-pause)
        Pg->>Tm: pause()
        Tm->>Se: pause()
    end

    opt usuário solicita parar
        Pr->>Pg: click(btn-stop)
        Pg->>Tm: stop()
        Tm->>Se: stop()
    end
```

---

## UC05 — Gerenciar Combos (Ruy)

### Diagrama de Atividades — UC05

```mermaid
flowchart TD
    Start([Início]) --> A0[Praticante: acessar Biblioteca de Combos]
    A0 --> A1[Sistema: listar combos cadastrados]
    A1 --> A2[Sistema: renderizar lista e formulário]
    A2 --> D0{Ação escolhida pelo praticante?}
    D0 -- "[sair]" --> End([Fim])
    D0 -- "[adicionar]" --> A3[Praticante: preencher nome e sequência]
    A3 --> A4[Praticante: acionar Adicionar]
    A4 --> D1{Nome vazio?}
    D1 -- "[sim]" --> E1[Sistema: exibir erro de nome vazio]
    E1 --> A2
    D1 -- "[não]" --> A5[Sistema: criar combo]
    A5 --> D2{Nome já existe na biblioteca?}
    D2 -- "[sim]" --> E2[Sistema: exibir erro de nome duplicado]
    E2 --> A2
    D2 -- "[não]" --> A6[Sistema: adicionar combo à biblioteca]
    A6 --> A7[Sistema: persistir estado]
    A7 --> A8[Sistema: re-renderizar lista]
    A8 --> D0
    D0 -- "[excluir]" --> A9[Praticante: acionar Excluir no item]
    A9 --> A10[Sistema: remover combo da biblioteca]
    A10 --> A11[Sistema: persistir estado]
    A11 --> A12[Sistema: re-renderizar lista]
    A12 --> D0
```

### Diagrama de Sequência — UC05

```mermaid
sequenceDiagram
    actor Pr as :Praticante
    participant Pg as :ComboLibraryPage
    participant St as :AppState
    participant Lib as :ComboLibrary
    participant Mg as :StorageManager
    participant Bk as :StorageBackend

    Pr->>Pg: abrir_pagina()
    Pg->>St: combo_library()
    St-->>Pg: lib:ComboLibrary
    Pg->>Lib: list_all()
    Lib-->>Pg: combos

    loop para cada combo em combos
        Pg->>Pg: montar linha do combo
    end
    Pg->>Pr: renderizar(lista + formulário)

    Note over Pr,Bk: seq — o praticante escolhe livremente as operações do CRUD

    opt Adicionar combo
        Pr->>Pg: preencher(name, sequence)
        Pr->>Pg: click(btn-add)
        create participant Cb as :Combo
        Pg->>Cb: new Combo(name, sequence)

        alt nome vazio
            Cb-->>Pg: ValueError("name must not be empty")
            Pg->>Pr: exibir_erro()
        else nome válido
            Pg->>Lib: add(combo)

            alt nome duplicado
                Lib-->>Pg: ValueError("already exists")
                Pg->>Pr: exibir_erro()
            else nome único
                Lib->>Lib: _combos.append(combo)
                Pg->>St: save()
                St->>St: to_dict()
                St->>Mg: save(APP_STATE_KEY, dict)
                Mg->>Bk: set_item(key, json)
                Pg->>Pg: rerender()
            end
        end
    end

    opt Excluir combo
        Pr->>Pg: click(btn-delete, name)
        Pg->>Lib: remove(name)

        opt nome inexistente
            Lib-->>Pg: KeyError
        end

        Pg->>St: save()
        St->>St: to_dict()
        St->>Mg: save(APP_STATE_KEY, dict)
        Mg->>Bk: set_item(key, json)
        Pg->>Pg: rerender()
    end
```
