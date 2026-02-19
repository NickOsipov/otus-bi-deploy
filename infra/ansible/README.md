# Ansible Playbooks для BI инфраструктуры

Набор Ansible playbook'ов для развертывания инфраструктуры бизнес-аналитики с Docker.

## Настройка

1. Отредактируйте файл `inventory.yml` и укажите IP-адреса ваших виртуальных машин:
   ```yaml
   redash-vm:
     ansible_host: YOUR_REDASH_IP  
   superset-vm:
     ansible_host: YOUR_SUPERSET_IP
   ```

2. Убедитесь, что у вас есть SSH доступ к виртуальным машинам и обновите путь к SSH ключу в `inventory.yml` и `ansible.cfg`.

## Использование

### 1. Установка Docker на все машины
```bash
cd /home/ono/otus/de/otus-bi-deploy/infra/ansible
ansible-playbook install-docker.yml
```

### 2. Клонирование репозитория на все машины
```bash
cd /home/ono/otus/de/otus-bi-deploy/infra/ansible
ansible-playbook clone-repo.yml
```

### Запуск для конкретной машины
```bash
ansible-playbook install-docker.yml --limit redash-vm
```

## Проверка

Проверить установку Docker:
```bash
ansible docker_hosts -m command -a "docker --version"
```

## Файлы

- `inventory.yml` - файл инвентаря с описанием хостов
- `ansible.cfg` - конфигурация Ansible
- `install-docker.yml` - playbook для установки Docker
- `clone-repo.yml` - playbook для клонирования/обновления репозитория
- `README.md` - этот файл с инструкциями
