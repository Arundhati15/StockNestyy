from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import StockForm, SignUpForm
from .models import Stock
import yfinance as yf
import json

# ---- Pages ----
def index(request):
    # Your simple live tester on the homepage still works
    return render(request, 'stock_app/index.html')

def watchlist(request):
    if request.user.is_authenticated:
        stocks = Stock.objects.filter(user=request.user)
    else:
        stocks = []
    return render(request, 'stock_app/watchlist.html', {'stocks': stocks})


@login_required
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            try:
                obj.save()
                messages.success(request, f"Added {obj.symbol} to your watchlist.")
                return redirect('watchlist')
            except Exception as e:
                messages.error(request, "This symbol already exists in your watchlist or is invalid.")
    else:
        form = StockForm()
    return render(request, 'stock_app/add_stock.html', {'form': form})


@login_required
def edit_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        form = StockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated watchlist item.")
            return redirect('watchlist')
    else:
        form = StockForm(instance=stock)
    return render(request, 'stock_app/edit_stock.html', {'form': form, 'stock': stock})

@login_required
def delete_stock(request, pk):
    stock = get_object_or_404(Stock, pk=pk, user=request.user)
    if request.method == 'POST':
        stock.delete()
        messages.success(request, "Deleted from watchlist.")
        return redirect('watchlist')
    return render(request, 'stock_app/confirm_delete.html', {'stock': stock})

def user_logout(request):
    logout(request)
    return redirect('login')  # redirect to login page after logout

# ---- Auth ----
'''   if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account was created.")
            return redirect('watchlist')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages'''

# Sign Up View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            return redirect("home")  # redirect to homepage
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

# Login View
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect("home")

# ---- APIs ----
def get_stock_data(request):
    symbol = (request.GET.get('symbol') or 'AAPL').strip().upper()
    try:
        hist = yf.download(symbol, period='2d', interval='1d', progress=False)
        if hist.empty:
            return JsonResponse({'error': 'Invalid symbol'}, status=400)
        price = float(hist['Close'].iloc[-1])
        prev  = float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
        change = price - prev
        pct = (change / prev * 100) if prev else 0.0
        return JsonResponse({
            'symbol': symbol,
            'price': round(price, 2),
            'prev_close': round(prev, 2),
            'change': round(change, 2),
            'changePct': round(pct, 2),
        })
    except Exception:
        return JsonResponse({'error': 'Fetch failed'}, status=500)

@login_required
def api_quotes(request):
    """Return quotes for CSV of symbols or for the logged-in user's watchlist."""
    csv = (request.GET.get('symbols') or '').upper()
    if csv:
        symbols = [s.strip() for s in csv.split(',') if s.strip()]
    else:
        symbols = list(Stock.objects.filter(user=request.user).values_list('symbol', flat=True))

    out = {}
    for sym in symbols:
        try:
            hist = yf.download(sym, period='2d', interval='1d', progress=False)
            if hist.empty:
                out[sym] = {'error': 'no_data'}
                continue
            price = float(hist['Close'].iloc[-1])
            prev  = float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
            change = price - prev
            pct = (change / prev * 100) if prev else 0.0
            out[sym] = {
                'price': round(price, 2),
                'prev_close': round(prev, 2),
                'change': round(change, 2),
                'changePct': round(pct, 2),
            }
        except Exception:
            out[sym] = {'error': 'fetch_failed'}
    return JsonResponse({'quotes': out})

@login_required
def stock_detail(request, symbol):
    return render(request, 'stock_app/stock_detail.html', {'symbol': symbol})

def api_history(request):
    """Return dates + close prices for Chart.js."""
    symbol = (request.GET.get('symbol') or 'AAPL').upper()
    period = request.GET.get('period') or '1mo'
    interval = request.GET.get('interval') or '1d'
    try:
        hist = yf.download(symbol, period=period, interval=interval, progress=False)
        if hist.empty:
            return JsonResponse({'error': 'no_data'}, status=400)
        dates = [i.strftime('%Y-%m-%d') for i in hist.index]
        closes = [round(float(x), 2) for x in hist['Close'].tolist()]
        return JsonResponse({'symbol': symbol, 'dates': dates, 'closes': closes})
    except Exception:
        return JsonResponse({'error': 'fetch_failed'}, status=500)
        # stock_app/views.py


# stock_app/views.py

def quick_quote(request):
    symbol = request.GET.get("symbol", None)
    if not symbol:
        return JsonResponse({"error": "No symbol provided"}, status=400)

    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        previous = stock.history(period="2d")["Close"].iloc[0]
        change = round(price - previous, 2)
        change_percent = round((change / previous) * 100, 2)

        return JsonResponse({
            "symbol": symbol.upper(),
            "price": round(price, 2),
            "change": change,
            "change_percent": change_percent
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





def stock_chart(request):
    symbol = request.GET.get('symbol', 'AAPL')  # default AAPL if none entered
    data = yf.download(symbol, period="1mo", interval="1d")

    dates = data.index.strftime('%Y-%m-%d').tolist()
    prices = data['Close'].squeeze().round(2).tolist()
    
    context = {
        'symbol': symbol,
        'dates': json.dumps(dates),
        'prices': json.dumps(prices)
    }
    return render(request, 'stock_app/stock_chart.html', context)

def chart_search(request):
    return render(request, 'stock_app/chart_search.html')




