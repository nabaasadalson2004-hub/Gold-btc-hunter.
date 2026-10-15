
//+------------------------------------------------------------------+
//|  BTC/Gold Hunter - Build Your Future - PURE CODE                 |
//|  24Hrs Demand/Supply Bot - Buy Demand, Sell Supply               |
//|  SL 30 pips, TP 60 pips, Auto Lot, Buy/Sell Day Detector         |
//+------------------------------------------------------------------+
#property copyright "Build Your Future - Hunter"
#property version   "1.00"
#property strict

#include <Trade/Trade.mqh>
CTrade trade;

input int Inp_StopLoss = 30;
input int Inp_TakeProfit = 60;

//--- Global
datetime lastTradeDay = 0;
bool isBuyDay = true;

//+------------------------------------------------------------------+
//| Lot Size Table - As Per Your Paper                               |
//+------------------------------------------------------------------+
double GetLotSize(double balance)
{
   if(balance >= 10 && balance <= 30) return 0.01;
   if(balance >= 31 && balance <= 40) return 0.02;
   if(balance >= 41 && balance <= 50) return 0.03;
   if(balance >= 51 && balance <= 60) return 0.04;
   if(balance >= 61 && balance <= 100) return 0.04;
   if(balance >= 101 && balance <= 200) return 0.05;
   if(balance >= 201 && balance <= 499) return 0.06;
   if(balance >= 500 && balance <= 999) return 0.10;
   if(balance >= 1000 && balance <= 2999) return 0.20;
   if(balance >= 3000 && balance <= 9999) return 0.40;
   if(balance >= 10000 && balance <= 49999) return 0.50;
   if(balance >= 50000 && balance <= 99999) return 1.50;
   if(balance >= 100000 && balance <= 999999) return 3.00;
   if(balance >= 1000000) return 10.0;
   return 0.01;
}

//+------------------------------------------------------------------+
//| Detect Buy Day or Sell Day                                       |
//+------------------------------------------------------------------+
bool DetectBuyDay()
{
   double maDaily = iMA(_Symbol, PERIOD_D1, 50, 0, MODE_EMA, PRICE_CLOSE);
   double price = iClose(_Symbol, PERIOD_D1, 1);
   if(price > maDaily) return true;
   return false;
}

//+------------------------------------------------------------------+
//| NFP Confirmation Filter                                          |
//+------------------------------------------------------------------+
bool NFP_Confirmation()
{
   MqlDateTime dt;
   TimeToStruct(TimeCurrent(), dt);
   if(dt.day_of_week == 5 && dt.day <= 7 && dt.hour >= 12 && dt.hour <= 16)
   {
      return false;
   }
   return true;
}

//+------------------------------------------------------------------+
//| Supply / Demand Zones                                            |
//+------------------------------------------------------------------+
bool IsDemandZone()
{
   double low1 = iLow(_Symbol, PERIOD_H1, 1);
   double low2 = iLow(_Symbol, PERIOD_H1, 2);
   double close = iClose(_Symbol, PERIOD_M5, 1);
   double open = iOpen(_Symbol, PERIOD_M5, 1);
   if(low1 <= low2 && close > open) return true;
   return false;
}

bool IsSupplyZone()
{
   double high1 = iHigh(_Symbol, PERIOD_H1, 1);
   double high2 = iHigh(_Symbol, PERIOD_H1, 2);
   double close = iClose(_Symbol, PERIOD_M5, 1);
   double open = iOpen(_Symbol, PERIOD_M5, 1);
   if(high1 >= high2 && close < open) return true;
   return false;
}

//+------------------------------------------------------------------+
//| Homepage Panel                                                   |
//+------------------------------------------------------------------+
void CreateHomepage()
{
   ObjectCreate(0, "BG", OBJ_RECTANGLE_LABEL, 0, 0, 0);
   ObjectSetInteger(0, "BG", OBJPROP_XDISTANCE, 10);
   ObjectSetInteger(0, "BG", OBJPROP_YDISTANCE, 20);
   ObjectSetInteger(0, "BG", OBJPROP_XSIZE, 300);
   ObjectSetInteger(0, "BG", OBJPROP_YSIZE, 400);
   ObjectSetInteger(0, "BG", OBJPROP_BGCOLOR, clrWhiteSmoke);
   
   ObjectCreate(0, "FutureText", OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, "FutureText", OBJPROP_XDISTANCE, 20);
   ObjectSetInteger(0, "FutureText", OBJPROP_YDISTANCE, 30);
   ObjectSetString(0, "FutureText", OBJPROP_TEXT, "Build your future");
   ObjectSetInteger(0, "FutureText", OBJPROP_FONTSIZE, 12);
   ObjectSetInteger(0, "FutureText", OBJPROP_COLOR, clrBlue);

   ObjectCreate(0, "BalBtn", OBJ_BUTTON, 0, 0, 0);
   ObjectSetInteger(0, "BalBtn", OBJPROP_XDISTANCE, 20);
   ObjectSetInteger(0, "BalBtn", OBJPROP_YDISTANCE, 60);
   ObjectSetInteger(0, "BalBtn", OBJPROP_XSIZE, 120);
   ObjectSetInteger(0, "BalBtn", OBJPROP_YSIZE, 25);
   ObjectSetString(0, "BalBtn", OBJPROP_TEXT, "Balance: $"+DoubleToString(AccountInfoDouble(ACCOUNT_BALANCE),2));

   ObjectCreate(0, "DepBtn", OBJ_BUTTON, 0, 0, 0);
   ObjectSetInteger(0, "DepBtn", OBJPROP_XDISTANCE, 150);
   ObjectSetInteger(0, "DepBtn", OBJPROP_YDISTANCE, 60);
   ObjectSetInteger(0, "DepBtn", OBJPROP_XSIZE, 120);
   ObjectSetInteger(0, "DepBtn", OBJPROP_YSIZE, 25);
   ObjectSetString(0, "DepBtn", OBJPROP_TEXT, "Deposit");
   ObjectSetInteger(0, "DepBtn", OBJPROP_BGCOLOR, clrGold);

   ObjectCreate(0, "MarketBox", OBJ_RECTANGLE_LABEL, 0, 0, 0);
   ObjectSetInteger(0, "MarketBox", OBJPROP_XDISTANCE, 20);
   ObjectSetInteger(0, "MarketBox", OBJPROP_YDISTANCE, 100);
   ObjectSetInteger(0, "MarketBox", OBJPROP_XSIZE, 260);
   ObjectSetInteger(0, "MarketBox", OBJPROP_YSIZE, 120);
   ObjectSetInteger(0, "MarketBox", OBJPROP_BGCOLOR, clrWhite);
}

//+------------------------------------------------------------------+
int OnInit()
{
   CreateHomepage();
   isBuyDay = DetectBuyDay();
   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
void OnTick()
{
   if(!NFP_Confirmation()) return;
   
   if(iTime(_Symbol, PERIOD_D1, 0) != lastTradeDay)
   {
      isBuyDay = DetectBuyDay();
      lastTradeDay = iTime(_Symbol, PERIOD_D1, 0);
   }

   if(PositionsTotal() == 0)
   {
      double balance = AccountInfoDouble(ACCOUNT_BALANCE);
      double lot = GetLotSize(balance);
      double price = SymbolInfoDouble(_Symbol, SYMBOL_ASK);
      double sl = 0, tp = 0;
      
      if(isBuyDay && IsDemandZone())
      {
         sl = price - Inp_StopLoss * 10 * _Point;
         tp = price + Inp_TakeProfit * 10 * _Point;
         trade.Buy(lot, _Symbol, 0, sl, tp, "Hunter Buy Demand");
      }
      else if(!isBuyDay && IsSupplyZone())
      {
         sl = price + Inp_StopLoss * 10 * _Point;
         tp = price - Inp_TakeProfit * 10 * _Point;
         trade.Sell(lot, _Symbol, 0, sl, tp, "Hunter Sell Supply");
      }
   }
}
