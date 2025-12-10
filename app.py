#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Word Start - Приложение для получения ключевых слов из Google Keyword Planner
Аналог Яндекс Word Start для Google Analytics/Ads
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
import requests
from typing import List, Dict, Optional

app = Flask(__name__)
CORS(app)

# Debug logging setup
LOG_PATH = '/root/андрей/жена/.cursor/debug.log'

def debug_log(hypothesis_id, location, message, data=None):
    """Write debug log to file"""
    try:
        log_entry = {
            "sessionId": "debug-session",
            "runId": "run1",
            "hypothesisId": hypothesis_id,
            "location": location,
            "message": message,
            "data": data or {},
            "timestamp": int(datetime.now().timestamp() * 1000)
        }
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    except Exception:
        pass  # Silent fail for logging

@app.before_request
def log_request():
    """Log all incoming requests"""
    # #region agent log
    debug_log("A", "app.py:before_request", "Incoming request", {
        "path": request.path,
        "method": request.method,
        "url": request.url,
        "remote_addr": request.remote_addr,
        "headers": dict(request.headers)
    })
    # #endregion

# Конфигурация
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['GOOGLE_ADS_API_KEY'] = os.environ.get('GOOGLE_ADS_API_KEY', '')
app.config['GOOGLE_ADS_CUSTOMER_ID'] = os.environ.get('GOOGLE_ADS_CUSTOMER_ID', '')

class GoogleKeywordPlanner:
    """Класс для работы с Google Keyword Planner API"""
    
    def __init__(self, api_key: str, customer_id: str):
        self.api_key = api_key
        self.customer_id = customer_id
        self.base_url = "https://googleads.googleapis.com/v16"
    
    def get_keyword_ideas(self, keywords: List[str], language_code: str = "ru", 
                         location_codes: List[str] = None) -> Dict:
        """
        Получить идеи ключевых слов из Google Keyword Planner
        
        Args:
            keywords: Список поисковых запросов
            language_code: Код языка (ru, en, uk и т.д.)
            location_codes: Коды локаций (например, ["2840"] для России)
        
        Returns:
            Словарь с данными о ключевых словах
        """
        # Коды локаций для разных стран
        location_map = {
            "2840": "2840",  # Россия
            "2336": "2336",  # Україна
            "2686": "2686",  # Беларусь
            "2826": "2826",  # Казахстан / Европа / Весь мир
            "2250": "2250",  # США
            "2825": "2825",  # Німеччина
        }
        
        if location_codes is None:
            location_codes = ["2840"]  # Россия по умолчанию
        else:
            # Преобразуем коды локаций
            location_codes = [location_map.get(str(code), str(code)) for code in location_codes]
        
        try:
            # Формируем запрос к Google Ads API
            # Примечание: Для реальной работы нужна OAuth аутентификация
            # Здесь показана структура запроса
            
            payload = {
                "customer_id": self.customer_id,
                "keyword_seed": {
                    "keywords": keywords
                },
                "language_constant": f"languageConstants/{language_code}",
                "geoTargetConstants": [f"geoTargetConstants/{code}" for code in location_codes],
                "include_adult_keywords": False
            }
            
            # В реальном приложении здесь будет запрос к Google Ads API
            # Для демо версии возвращаем моковые данные
            return self._mock_keyword_data(keywords)
            
        except Exception as e:
            return {
                "error": str(e),
                "keywords": []
            }
    
    def _mock_keyword_data(self, keywords: List[str]) -> Dict:
        """Моковые данные для демонстрации (заменить на реальный API вызов)"""
        results = []
        
        for keyword in keywords:
            # Генерируем похожие ключевые слова
            variations = [
                f"{keyword} купить",
                f"{keyword} цена",
                f"{keyword} отзывы",
                f"{keyword} онлайн",
                f"лучший {keyword}",
                f"{keyword} 2025",
                f"как выбрать {keyword}",
                f"{keyword} бесплатно"
            ]
            
            for variation in variations:
                # Генерируем случайные метрики
                import random
                results.append({
                    "keyword": variation,
                    "avg_monthly_searches": random.randint(100, 100000),
                    "competition": random.choice(["LOW", "MEDIUM", "HIGH"]),
                    "competition_index": random.randint(0, 100),
                    "low_top_of_page_bid": random.randint(10, 500),
                    "high_top_of_page_bid": random.randint(500, 2000),
                    "relevance": random.randint(70, 100)
                })
        
        return {
            "keywords": results,
            "total_count": len(results),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_keyword_metrics(self, keyword: str) -> Dict:
        """Получить метрики для конкретного ключевого слова"""
        try:
            # Реальный API вызов здесь
            return {
                "keyword": keyword,
                "avg_monthly_searches": 1000,
                "competition": "MEDIUM",
                "competition_index": 50,
                "low_top_of_page_bid": 50,
                "high_top_of_page_bid": 200
            }
        except Exception as e:
            return {"error": str(e)}


# Инициализация
keyword_planner = GoogleKeywordPlanner(
    app.config['GOOGLE_ADS_API_KEY'],
    app.config['GOOGLE_ADS_CUSTOMER_ID']
)


@app.route('/')
@app.route('/thamini/wordstart/')
@app.route('/thamini/wordstart')
def index():
    """Главная страница приложения"""
    # #region agent log
    debug_log("C", "app.py:index", "Index route called", {
        "path": request.path,
        "route": request.endpoint
    })
    # #endregion
    result = render_template('index.html')
    # #region agent log
    debug_log("C", "app.py:index", "Index route response", {
        "status": "ok",
        "content_length": len(result) if result else 0
    })
    # #endregion
    return result


@app.route('/api/keywords', methods=['POST'])
@app.route('/thamini/wordstart/api/keywords', methods=['POST'])
def get_keywords():
    """API endpoint для получения ключевых слов"""
    # #region agent log
    debug_log("C", "app.py:get_keywords", "Keywords route called", {
        "path": request.path,
        "method": request.method,
        "route": request.endpoint
    })
    # #endregion
    try:
        data = request.get_json()
        # #region agent log
        debug_log("C", "app.py:get_keywords", "Request data received", {
            "has_data": data is not None,
            "data_keys": list(data.keys()) if data else []
        })
        # #endregion
        search_queries = data.get('queries', [])
        language = data.get('language', 'ru')
        location = data.get('location', ['2840'])  # Россия по умолчанию
        
        if not search_queries:
            # #region agent log
            debug_log("C", "app.py:get_keywords", "Validation failed - no queries", {})
            # #endregion
            return jsonify({
                "error": "Не указаны поисковые запросы",
                "keywords": []
            }), 400
        
        # Получаем ключевые слова
        result = keyword_planner.get_keyword_ideas(
            keywords=search_queries,
            language_code=language,
            location_codes=location
        )
        # #region agent log
        debug_log("C", "app.py:get_keywords", "Keywords result", {
            "keywords_count": len(result.get('keywords', [])),
            "has_error": 'error' in result
        })
        # #endregion
        
        return jsonify(result)
        
    except Exception as e:
        # #region agent log
        debug_log("C", "app.py:get_keywords", "Exception occurred", {
            "error": str(e),
            "error_type": type(e).__name__
        })
        # #endregion
        return jsonify({
            "error": str(e),
            "keywords": []
        }), 500


@app.route('/api/keyword/<keyword>', methods=['GET'])
def get_keyword_details(keyword):
    """API endpoint для получения детальной информации о ключевом слове"""
    try:
        result = keyword_planner.get_keyword_metrics(keyword)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_keywords():
    """API endpoint для экспорта ключевых слов"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', [])
        format_type = data.get('format', 'json')  # json, csv, txt
        
        if format_type == 'csv':
            csv_content = "Ключевое слово,Средние запросы в месяц,Конкуренция,Конкуренция индекс,Мин. ставка,Макс. ставка\n"
            for kw in keywords:
                csv_content += f"{kw.get('keyword', '')},{kw.get('avg_monthly_searches', 0)},{kw.get('competition', '')},{kw.get('competition_index', 0)},{kw.get('low_top_of_page_bid', 0)},{kw.get('high_top_of_page_bid', 0)}\n"
            
            return csv_content, 200, {'Content-Type': 'text/csv; charset=utf-8'}
        
        elif format_type == 'txt':
            txt_content = "\n".join([kw.get('keyword', '') for kw in keywords])
            return txt_content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        
        else:  # json
            return jsonify(keywords)
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
@app.route('/thamini/wordstart/health', methods=['GET'])
def health():
    """Health check endpoint"""
    # #region agent log
    debug_log("B", "app.py:health", "Health route called", {
        "path": request.path,
        "method": request.method,
        "route": request.endpoint,
        "remote_addr": request.remote_addr
    })
    # #endregion
    result = jsonify({
        "status": "ok",
        "timestamp": datetime.now().isoformat()
    })
    # #region agent log
    debug_log("B", "app.py:health", "Health route response", {
        "status_code": 200,
        "response_data": result.get_data(as_text=True)[:100]
    })
    # #endregion
    return result


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 40005))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    # #region agent log
    debug_log("B", "app.py:main", "Application starting", {
        "port": port,
        "host": "0.0.0.0",
        "debug": debug
    })
    # #endregion
    app.run(host='0.0.0.0', port=port, debug=debug)

